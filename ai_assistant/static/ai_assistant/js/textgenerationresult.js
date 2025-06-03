class TextToSpeech {
    constructor() {
        this.synth = window.speechSynthesis;
        this.utterance = null;
        this.isPlaying = false;
        
        this.listenBtn = document.getElementById('listenBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.wave = document.getElementById('wave');
        this.storyContent = document.getElementById('story-content');
        
        this.initialize();
    }

    initialize() {
        if (!this.synth) {
            console.log('Speech synthesis not supported');
            this.listenBtn.disabled = true;
            return;
        }

        this.listenBtn.addEventListener('click', () => this.start());
        this.stopBtn.addEventListener('click', () => this.stop());
        
       
    }

    start() {
    if (this.isPlaying) return;

    this.utterance = new SpeechSynthesisUtterance(this.storyContent.textContent);

    // Attach the onend event to the utterance
    this.utterance.onend = () => {
        this.toggleUI(false);
    };

    this.synth.speak(this.utterance);
    this.toggleUI(true);
   }


    stop() {
        if (this.synth.speaking) {
            this.synth.cancel();
            this.toggleUI(false);
        }
    }

    toggleUI(playing) {
        this.isPlaying = playing;
        this.listenBtn.classList.toggle('d-none', playing);
        this.stopBtn.classList.toggle('d-none', !playing);
        this.wave.classList.toggle('d-none', !playing);
    }
}

// Initialize when document loads
document.addEventListener('DOMContentLoaded', () => {
    new TextToSpeech();
});