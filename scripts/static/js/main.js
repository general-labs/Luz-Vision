'use strict';

const numberOfBurstShot = 5;
const apiURL = ``;
  // const apiURL = `post.php`;

var constraints = {
  audio: false,
  video: {
    width: { min: 1280 },
    height: { min: 720 },
    facingMode: { exact: "environment" } // Rear Camera
    //facingMode: "user" // Front Camera
  }
}

const video = document.querySelector('video');
const canvas = window.canvas = document.querySelector('canvas');
const captureButton = document.getElementById('capture_shot');
const burstShotButton = document.getElementById('burst_shot');
const inputTextBox = document.getElementById('text_to_speech');
const findObject = document.getElementById("find_object");
const detectObject = document.getElementById("detect_object");
const objectData = document.getElementById("object_data");

canvas.width = 480;
canvas.height = 360;

function speakText(txt) {

  if (!txt) {
    return;
  }
  console.log(txt);
  
  window.speechSynthesis.cancel();
  
  window.msg = new SpeechSynthesisUtterance(txt);
  msg.rate = 0.9; // 0.1 to 10
  if (navigator.userAgent.match(/(iPad|iPhone|iPod touch)/i)) {
    // iPhone speech rate is much faster, for some reason
    msg.rate = 0.3;
  }
  msg.lang = 'en-US';
  // var voices = window.speechSynthesis.getVoices();
  // msg.voice = voices[0];
  window.speechSynthesis.speak(msg);

}

const text2SpeechLoop = () => {
  setInterval(function () {
    if (inputTextBox.value != "") {
      speakText(inputTextBox.value);
      inputTextBox.value = "";
    }
    

  }, 3000);
}

const identifyObjPost = () => {
  $.ajax({
    url: `${apiURL}/predict_image`,
    crossDomain: true,
    data: { url: canvas.toDataURL("image/png") },
    type: "POST",
    success: function(dataR) {
      console.log("Success: ", dataR);
      let dataOutput = dataR.Prediction.toString();
      inputTextBox.value = dataOutput || "";
      objectData.innerHTML = dataOutput || "";
    },
    error: function(xhr, status, error) {
      console.log("Error: " + error.message);
    }
  });
}

const explainEnv = () => {
  $.ajax({
    url: `${apiURL}/image_caption`,
    crossDomain: true,
    data: { url: canvas.toDataURL("image/png") },
    type: "POST",
    success: function(dataR) {
      console.log("Success: " + dataR.captions);
      let dataOutput = dataR.captions.toString();
      let firstItem = dataOutput.split(",");
      inputTextBox.value = firstItem[0] || "";
      objectData.innerHTML = firstItem[0] || "";
    },
    error: function(xhr, status, error) {
      console.log("Error: " + error.message);
    }
  });
};

const objectDetails = () => {
  copyImageFromCamera();
  speakText("Please wait");
  identifyObjPost();
}

const copyImageFromCamera = () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
}

const takeShot = (inputData, image_folder = 'train') => {
  copyImageFromCamera();
  // Create Blank To Bypass User Interfaction Restriction.
  speakText('Please wait');
  explainEnv();
}

burstShotButton.onclick = function () {
  let counter = 0;
  setInterval(function () {
    if (counter < numberOfBurstShot) {
      takeShot('no-name-x', 'test');
    }
    counter++;
  }, 3000);
};

captureButton.onclick = function () {
  var inputData = prompt("Please enter what is it about?", "table");
  text2SpeechLoop();
  takeShot(inputData, 'train');
};

findObject.onclick = function() {
  text2SpeechLoop();
  takeShot('', "");
};


detectObject.onclick = function() {
  text2SpeechLoop();
  objectDetails();
};


function handleSuccess(stream) {
  window.stream = stream; // make stream available to browser console
  video.srcObject = stream;
}

function handleError(error) {
  console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
}

navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);














