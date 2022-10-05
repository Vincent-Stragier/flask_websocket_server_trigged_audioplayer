$(document).ready(function () {
    var socket = io.connect();

    // makes playing audio return a promise
    // function blocking_play(audio){
    //     return new Promise(res=>{
    //     audio.loop = false;
    //     audio.play()
    //     audio.onended = res
    //     })
    // }
  
    //   // how to call
    //   async function test(){
    //     const audio = new Audio('<url>')
    //     await playAudio(audio)
    //     // code that will run after audio finishes...
    //   }

    socket.on("audio", function (msg) {
        console.log("Received audio control :: " + msg.control);
        // console.log("Received audio file :: " + msg.file);
        if (msg.control === "play") {
            console.log("<play audio>")
            const blob = new Blob([msg.file], { type: "audio/mp3" });
            const audio_url = window.URL.createObjectURL(blob);
            console.log(audio_url)
            var audio = new Audio(audio_url);
            audio.loop = false;
            // Warning: this is an asynchronous method
            // May not work until the user authorize/unmute the audio for the website
            audio.play()
            // window.URL.revokeObjectURL(audio_url);
            console.log("<audio 'played'>")
        }
    });
});
