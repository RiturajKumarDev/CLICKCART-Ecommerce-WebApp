function addMoreImage() {
    let imgs = document.querySelector(".imgs");
    let imgNo = imgs.lastElementChild.children[0].id;
    imgNo = Number(imgNo.match(/\d+/g)) + 1;
    console.log(imgNo)
    let temp = document.createElement("label");
    temp.className = "img";
    temp.setAttribute("for", `img${imgNo}`);
    temp.innerHTML = `<input type="file" name="img${imgNo}" id="img${imgNo}" required accept="images/*">
                              <p>Upload image</p>`;
    imgs.appendChild(temp);
}

function addMoreVid() {
    let vids = document.querySelector(".vids");
    let vidNo = vids.lastElementChild.children[0].id;
    vidNo = Number(vidNo.match(/\d+/g)) + 1;
    console.log(vidNo)
    let temp = document.createElement("label");
    temp.className = "vid";
    temp.setAttribute("for", `vid${vidNo}`);
    temp.innerHTML = `<input type="file" name="vid${vidNo}" id="vid${vidNo}" required accept="video/*">
                              <p>Upload video</p>`;
    vids.appendChild(temp);
}

function addMoreKeyFeature() {
    let keysFeatures = document.querySelector(".keys-features");
    let keysFeaturesNo = keysFeatures.lastElementChild.children[0].className;
    keysFeaturesNo = Number(keysFeaturesNo.match(/\d+/g)) + 1;
    console.log(keysFeaturesNo)
    let temp = document.createElement("div");
    temp.className = "key-feature";
    temp.innerHTML = `<input type="text" name="key${keysFeaturesNo}" class="key${keysFeaturesNo}" placeholder="Key" required><br>
                              <input type="text" name="feature${keysFeaturesNo}" class="key${keysFeaturesNo}" placeholder="Feature" required>`;
    keysFeatures.appendChild(temp);
}
