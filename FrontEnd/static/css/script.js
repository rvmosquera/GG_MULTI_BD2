var videoWidth = 420;
            var videoHeight = 340;
            var videoTag = document.getElementById('theVideo');
            var canvasTag = document.getElementById('theCanvas');
            var btnCapture = document.getElementById("btnCapture");
            var btnDownloadImage = document.getElementById("btnDownloadImage");
            videoTag.setAttribute('width', videoWidth);
            videoTag.setAttribute('height', videoHeight);
            canvasTag.setAttribute('width', videoWidth);
            canvasTag.setAttribute('height', videoHeight);
            window.onload = () => {
                navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: {
                        width: videoWidth,
                        height: videoHeight
                    }
                }).then(stream => {
                    videoTag.srcObject = stream;
                }).catch(e => {
                    document.getElementById('errorTxt').innerHTML = 'ERROR: ' + e.toString();
                });
                var canvasContext = canvasTag.getContext('2d');
                btnCapture.addEventListener("click", () => {
                    canvasContext.drawImage(videoTag, 0, 0, videoWidth, videoHeight);
                });
                btnDownloadImage.addEventListener("click", () => {
                    var link = document.createElement('a');
                    link.download = 'capturedImage.png';
                    link.href = canvasTag.toDataURL();
                    link.click();
                });
            };