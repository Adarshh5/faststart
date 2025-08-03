document.addEventListener('DOMContentLoaded', function () {
    const listenBtn = document.getElementById('listen-btn');
    const stopBtn = document.getElementById('stop-btn');
    const voiceAnim = document.getElementById('voice-animation');
    const storyContent = document.getElementById('story-content');

    let synth = window.speechSynthesis;
    let utterance;

    listenBtn?.addEventListener('click', function () {
        if (!synth.speaking) {
            utterance = new SpeechSynthesisUtterance(storyContent.innerText);
            utterance.onend = () => {
                stopBtn.classList.add('d-none');
                listenBtn.classList.remove('d-none');
                voiceAnim.classList.add('d-none');
            };
            synth.speak(utterance);
            listenBtn.classList.add('d-none');
            stopBtn.classList.remove('d-none');
            voiceAnim.classList.remove('d-none');
        }
    });

    stopBtn?.addEventListener('click', function () {
        if (synth.speaking) {
            synth.cancel();
        }
        stopBtn.classList.add('d-none');
        listenBtn.classList.remove('d-none');
        voiceAnim.classList.add('d-none');
    });
});
