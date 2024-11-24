document.addEventListener('DOMContentLoaded', () => {
    const cameraToggles = {
        0: document.getElementById('camera1-toggle'),
        2: document.getElementById('camera2-toggle'),
        4: document.getElementById('camera3-toggle'),
    };

    const cameraFeeds = {
        0: document.getElementById('camera1-feed'),
        2: document.getElementById('camera2-feed'),
        4: document.getElementById('camera3-feed'),
    };

    const userInput = document.getElementById("user-input");
    const volumeDisplay = document.getElementById("volume-display");
    const volumeBar = document.getElementById("volume-bar");
    const micToggle = document.getElementById("speech-recognition");

    const sockets = {};
    let currentLabel = "None";
    let noFaceTimer = null;
    let countdownInterval = null; // 카운트다운 인터벌
    const NO_FACE_TIMEOUT = 5000;
    const COUNTDOWN_SECONDS = 5; 

    let resetTimer = null;
    let isMicOn = false;
    let audioSocket;

    // WebSocket for notifications
    const notificationSocket = new WebSocket(`ws://${window.location.host}/ws/notifications`);

    notificationSocket.onmessage = (event) => {
        const message = event.data;
        addBotMessage(message); // Add AI message to chat box
    };

    notificationSocket.onclose = () => {
        console.log("Notification WebSocket closed.");
    };

    notificationSocket.onerror = (error) => {
        console.error("Notification WebSocket error:", error);
    };

    function startCamera(cameraId) {
        sockets[cameraId] = new WebSocket(`ws://${window.location.host}/ws/stream/${cameraId}`);

        sockets[cameraId].onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.error) {
                console.error(`Camera ${cameraId}: ${data.error}`);
                return;
            }

            const img = cameraFeeds[cameraId];
            img.src = `data:image/jpeg;base64,${data.frame}`;

            if (cameraId === 0 && data.label) {
                handleFaceData(data.label);
            }
        };

        sockets[cameraId].onclose = () => console.log(`Camera ${cameraId} WebSocket closed.`);
        sockets[cameraId].onerror = (error) => console.error(`Camera ${cameraId} WebSocket error:`, error);
    }

    function stopCamera(cameraId) {
        if (sockets[cameraId]) {
            sockets[cameraId].close();
            delete sockets[cameraId];
        }
        if (cameraFeeds[cameraId]) {
            cameraFeeds[cameraId].src = '';
        }
    }

    function toggleCamera(cameraId) {
        const toggle = cameraToggles[cameraId];
        if (!toggle) {
            console.error(`Toggle for camera ${cameraId} not found.`);
            return;
        }

        if (toggle.checked) {
            startCamera(cameraId);
        } else {
            stopCamera(cameraId);
        }
    }

    for (let id in cameraToggles) {
        cameraToggles[id].addEventListener('change', () => toggleCamera(parseInt(id)));
    }

    function handleFaceData(label) {
        if (label === "None") {
            // 얼굴이 사라진 경우 타이머 시작
            startNoFaceTimer();

        } else {
            resetNoFaceTimer(); // 얼굴이 다시 나타나면 타이머 초기화


            if (currentLabel !== label) {
                currentLabel = label;
                const faceLabel = document.getElementById('face-label');
                const chatBox = document.getElementById('chat-box');

                faceLabel.textContent = label === "Unknown" 
                    ? "고객님 첫 방문을 환영합니다." 
                    : `고객님 재방문을 환영합니다.`;

                chatBox.innerHTML = "";

                if (label === "Unknown") {
                    addBotMessage("환영합니다! 저는 AI 주문 접수원입니다.");
                    addBotMessage("회원가입을 하시면 더 많은 혜택을 받으실 수 있어요.");
                    addBotMessage("회원가입 하시겠어요?");
                } else {
                    addBotMessage(`반갑습니다, 고객님! 주문을 도와드리겠습니다.`);
                }
                
            }
        }
    }

    function startNoFaceTimer() {
        if (noFaceTimer) return;
    
        let countdown = COUNTDOWN_SECONDS;
        const countdownTimer = document.getElementById('countdown-timer');
        countdownTimer.textContent = `로그아웃까지 ${countdown}초`;
    
        noFaceTimer = setTimeout(() => {
            if (currentLabel === "Unknown") {
                deleteUnknownSession();
            }
    
            clearChat();
    
            document.getElementById('face-label').textContent = "Detected Face: None";
            currentLabel = "None"; // 현재 라벨을 초기화
            countdownTimer.textContent = "";
        }, NO_FACE_TIMEOUT);
    
        countdownInterval = setInterval(() => {
            countdown -= 1;
            if (countdown > 0) {
                countdownTimer.textContent = `로그아웃까지 ${countdown}초`;
            } else {
                clearInterval(countdownInterval);
                countdownTimer.textContent = "";
            }
        }, 2000);
    }

    function resetNoFaceTimer() {
        if (noFaceTimer) {
            clearTimeout(noFaceTimer);
            noFaceTimer = null;
        }
        if (countdownInterval) {
            clearInterval(countdownInterval);
            countdownInterval = null;
        }
        const countdownTimer = document.getElementById('countdown-timer');
        countdownTimer.textContent = "";
    }

    function clearChat() {
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML = "";
    }

    async function deleteUnknownSession() {
        try {
            const response = await fetch("/chatbot/delete_session", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ session_id: "Unknown" })
            });

            if (!response.ok) {
                throw new Error("Failed to delete session");
            }

            console.log("Unknown User chatHistory deleted successfully.");
        } catch (error) {
            console.error("Error deleting Unknown session:", error);
        }
    }

    function addBotMessage(message) {
        const chatBox = document.getElementById("chat-box");
        const messageDiv = document.createElement("div");
        messageDiv.className = "message bot";
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const userInput = document.getElementById("user-input");
        const message = userInput.value.trim();

        if (message) {
            addMessage("user", message);
            userInput.value = "";

            try {
                const response = await fetch("/chatbot/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        question: message,
                        session_id: currentLabel
                    })
                });

                if (!response.ok) {
                    throw new Error("서버 응답 실패");
                }

                const data = await response.json();
                addMessage("bot", data.answer);
            } catch (error) {
                console.error("Error:", error);
                addMessage("bot", "에러가 발생했습니다. 다시 시도해주세요.");
            }
        }
    }

    function addMessage(sender, text) {
        const chatBox = document.getElementById("chat-box");
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function initializeAudioSocket() {
        if (audioSocket) {
            audioSocket.close();
        }

        audioSocket = new WebSocket(`ws://${window.location.host}/ws`);

        audioSocket.onmessage = (event) => {
            const data = event.data;

            // 볼륨 데이터 처리
            if (data.startsWith("volume:")) {
                const volume = parseInt(data.split(":")[1], 10);

                // 볼륨 디스플레이 및 게이지 바 업데이트
                volumeDisplay.textContent = `Volume: ${volume}%`;
                volumeBar.style.width = `${volume}%`;

                // 볼륨이 50 이상일 때 강조 표시
                if (volume >= 50) {
                    userInput.style.border = `3px solid red`; // 두꺼운 빨간색 테두리
                    userInput.classList.add("highlight");

                    // 강조 효과 일정 시간 후 제거
                    if (resetTimer) {
                        clearTimeout(resetTimer);
                    }
                    resetTimer = setTimeout(() => {
                        userInput.style.border = ""; // 테두리 초기화
                        userInput.classList.remove("highlight");
                    }, 500);
                } else {
                    // 볼륨이 낮으면 강조 제거
                    userInput.style.border = "";
                    userInput.classList.remove("highlight");
                }
            } else if (data.startsWith("text:")) {
                // 음성 텍스트 데이터 처리
                const text = data.split(":")[1];
                userInput.value = text; // 입력창에 텍스트 표시
                sendMessage(); // 텍스트를 자동으로 전송
            }
        };

        audioSocket.onclose = () => {
            console.log("Audio WebSocket closed.");
        };

        audioSocket.onerror = (error) => {
            console.error("Audio WebSocket error:", error);
        };
    }

    micToggle.addEventListener("change", (e) => {
        isMicOn = e.target.checked;

        if (isMicOn) {
            initializeAudioSocket();
            console.log("Microphone enabled, WebSocket initialized.");
        } else {
            if (audioSocket) {
                audioSocket.close();
                console.log("Microphone disabled, WebSocket closed.");
            }
        }
    });


    function handleKeyPress(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }

    // 사용자 입력창에 이벤트 바인딩
    document.getElementById("user-input").addEventListener("keypress", handleKeyPress);
    document.getElementById("send-button").addEventListener("click", sendMessage);
    document.getElementById("speech-recognition").addEventListener("change", async (e) => {
        isMicOn = e.target.checked;
    });

});
