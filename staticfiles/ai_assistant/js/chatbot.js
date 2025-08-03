


document.addEventListener("DOMContentLoaded", function () {
      const chatBox = document.getElementById("chatBox");
      const chatForm = document.getElementById("chatForm");
      const userInput = document.getElementById("userInput");
      const speakBtn = document.getElementById("speakBtn");
      const messageCount = document.getElementById("messageCount");
      const typingIndicator = document.getElementById("typingIndicator");
      let currentMessageCount = 0;
      let recognition;
      let isListening = false;
      let isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

      
      const textarea = document.getElementById("userInput");
      textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = Math.min(this.scrollHeight, 72) + "px"; // 72px ~ 3 lines
      });

      // Initialize message count
      if (messageCount) {
          currentMessageCount = parseInt('{{ user_chat_timing.count|default:0 }}') || 0;
          updateMessageCount();
      }

      // Initialize speech recognition if available
      if ('webkitSpeechRecognition' in window) {
          recognition = new webkitSpeechRecognition();
          recognition.lang = 'en-US';
          recognition.continuous = false;
          recognition.interimResults = false;

          recognition.onresult = function (event) {
              const transcript = event.results[0][0].transcript;
              userInput.value = transcript;
              speakBtn.innerHTML = '<i class="fas fa-microphone"></i>';
              speakBtn.classList.remove("listening");
          };

          recognition.onerror = function (event) {
              console.error("Speech recognition error:", event.error);
              speakBtn.innerHTML = '<i class="fas fa-microphone"></i>';
              speakBtn.classList.remove("listening");
          };

          recognition.onend = function () {
              isListening = false;
              speakBtn.innerHTML = '<i class="fas fa-microphone"></i>';
              speakBtn.classList.remove("listening");
          };
      } else {
          speakBtn.disabled = true;
          speakBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
          speakBtn.title = "Voice not supported";
      }

      // Voice input handler
      speakBtn.addEventListener("click", function () {
          if (!recognition) return;
          
          if (!isListening) {
              recognition.start();
              isListening = true;
              speakBtn.innerHTML = '<i class="fas fa-circle"></i>';
              speakBtn.classList.add("listening");
          } else {
              recognition.stop();
          }
      });

      let isWaitingForResponse = false;

      chatForm.addEventListener("submit", function (e) {
          e.preventDefault();

          if (isWaitingForResponse) {
              showAlert("⏳ Please wait for the AI to respond.");
              return;
          }

          const message = userInput.value.trim();
          const wordCount = message.split(/\s+/).filter(word => word.length > 0).length;
          
          if (wordCount > 300) {
              showAlert(`❌ You have exceeded the 300-word limit. Your message has ${wordCount} words.`);
              return;
          }

          if (!message) return;

          if (currentMessageCount >= 20) {
              showAlert("⛔ You have reached your message limit (20 messages)");
              return;
          }

          // Disable input while waiting for response
          isWaitingForResponse = true;
          userInput.disabled = true;
          const sendButton = chatForm.querySelector('button[type="submit"]');
          if (sendButton) sendButton.disabled = true;

          // Hide input on mobile during response
          if (isMobile) {
              document.querySelector('.chat-input-area').style.display = 'none';
              typingIndicator.style.display = 'flex';
          }

          appendMessage("user", message);
          userInput.value = "";
          currentMessageCount++;
          updateMessageCount();
          scrollToBottom();

          const fetchUrl = chatForm.dataset.url;

          fetch(fetchUrl, {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": getCookie("csrftoken"),
              },
              body: JSON.stringify({ user_message: message }),
          })
          .then((response) => response.json())
          .then((data) => {
              if (data.error) {
                  appendMessage("ai", `⚠️ Error: ${data.error}`);
              } else {
                  appendMessage("ai", data.reply, data.translation);
                  speakText(data.reply);
              }
          })
          .catch((error) => {
              appendMessage("ai", "⚠️ Sorry, something went wrong.");
              console.error("Error:", error);
          })
          .finally(() => {
              // Re-enable input and button
              isWaitingForResponse = false;
              userInput.disabled = false;
              if (sendButton) sendButton.disabled = false;
              
              // Show input area again
              if (isMobile) {
                  document.querySelector('.chat-input-area').style.display = 'block';
                  typingIndicator.style.display = 'none';
              }
              
              // Don't auto-focus on mobile
              if (!isMobile) {
                  userInput.focus();
              }
          });
      });

      // Append message to chat
      function appendMessage(type, text, translation = null) {
          const messageDiv = document.createElement("div");
          messageDiv.classList.add("message", type);
          messageDiv.textContent = text;
          
          if (translation && type === "ai") {
              const translationDiv = document.createElement("div");
              translationDiv.classList.add("translation");
              translationDiv.textContent = translation;
              messageDiv.appendChild(translationDiv);
          }
          
          chatBox.insertBefore(messageDiv, typingIndicator);
          scrollToBottom();
      }

      // Update message counter
      function updateMessageCount() {
          if (!messageCount) return;
          messageCount.textContent = `${currentMessageCount}/20`;
          
          // Update data attribute for styling
          messageCount.parentElement.setAttribute('data-count', currentMessageCount);
          
          // Change color when approaching limit
          if (currentMessageCount >= 16) {
              messageCount.style.color = "#ff6b6b";
          } else {
              messageCount.style.color = "inherit";
          }
      }

      function speakText(text) {
          if ('speechSynthesis' in window) {
              // Wait for voices to be loaded
              const loadVoices = () => {
                  const voices = speechSynthesis.getVoices();

                  if (voices.length === 0) {
                      // Voices not yet loaded, try again shortly
                      return setTimeout(() => loadVoices(), 100);
                  }

                  // Try to pick a female English voice
                  const femaleVoice = voices.find(voice =>
                      voice.lang.startsWith('en') &&
                      (voice.name.toLowerCase().includes('female') ||
                      voice.name.toLowerCase().includes('woman') ||
                      voice.name.toLowerCase().includes('zira') ||
                      voice.name.toLowerCase().includes('samantha') ||
                      voice.name.toLowerCase().includes('google')
                      )
                  );

                  const utterance = new SpeechSynthesisUtterance(text);
                  utterance.lang = 'en-US';
                  utterance.rate = 0.85;

                  if (femaleVoice) {
                      utterance.voice = femaleVoice;
                  }

                  speechSynthesis.speak(utterance);
              };

              loadVoices();
          }
      }

      // Scroll to bottom of chat
      function scrollToBottom() {
          chatBox.scrollTop = chatBox.scrollHeight;
      }

      // Get CSRF token
      function getCookie(name) {
          const value = `; ${document.cookie}`;
          const parts = value.split(`; ${name}=`);
          if (parts.length === 2) return parts.pop().split(";").shift();
      }

      // Show alert message
      function showAlert(message) {
          const alertDiv = document.createElement("div");
          alertDiv.classList.add("alert-message");
          alertDiv.textContent = message;
          
          document.body.appendChild(alertDiv);
          setTimeout(() => {
              alertDiv.remove();
          }, 3000);
      }

      // Initial scroll to bottom
      scrollToBottom();
        
     
  });
