function showRoomData(path, oldValue, oldUnits) {
    let overlay = $('#floor-plan-overlay');
    let currentD = overlay.attr('d');
    let pathD = $(path).attr('d');
    overlay.attr('d', currentD + ' ' + pathD);
    overlay.css({'opacity': 0.6, 'visibility': 'visible'});

    let room = $(path).attr('id').split("-")[2];
    // Extract the coordinates, width, and height, from the path
    let splitPath = pathD.split(" ");
    let bottomRightCorner = [parseFloat(splitPath[4].substr(1)), parseFloat(splitPath[5])];
    let cornerPadding = 50;
    let boxPadding = 150;
    let textPadding = 50;

    // Move text and fill in with value
    let roomText = $('#room-title-text');
    let valueText = $('#room-value-text');

    let roomTextCoords = [bottomRightCorner[0] + cornerPadding + boxPadding / 4, bottomRightCorner[1] + cornerPadding];

    roomText.attr('x', roomTextCoords[0]);
    roomText.attr('y', roomTextCoords[1]);
    roomText.css('visibility', 'visible');
    roomText.html('​Room ' + room);

    let roomTextBBox = document.getElementById('room-title-text').getBBox();

    let valueTextCoords = [bottomRightCorner[0] + cornerPadding + boxPadding / 4, bottomRightCorner[1] + cornerPadding + roomTextBBox.height + textPadding];

    valueText.attr('x', valueTextCoords[0]);
    valueText.attr('y', valueTextCoords[1]);
    valueText.css('visibility', 'visible');
    valueText.html(`${isShowingTemperature ? 'Temperature' : 'CO2 Level' }: ${oldValue} ${oldUnits}`);

    // Move and show the svg box
    let box = $('#value-box');
    let boxCoords = [valueTextCoords[0] - boxPadding / 4, roomTextCoords[1] - roomTextBBox.height - textPadding / 2];

    box.attr('x', boxCoords[0]);
    box.attr('y', boxCoords[1]);
    box.attr('height', 4 * textPadding + roomTextBBox.height + document.getElementById('room-value-text').getBBox().height);
    box.attr('width', 3 * boxPadding / 4 + document.getElementById('room-value-text').getBBox().width);
    box.css('fill', 'white');
    box.css('stroke', 'black');
    box.css('stroke-width', '4');
    box.css('visibility', 'visible');
}

function hideRoomData(path) {
    let overlay = $('#floor-plan-overlay');
    let currentD = overlay.attr('d');
    overlay.attr('d', currentD.split("Z")[0] + "Z");
    overlay.css({'opacity': 0, 'visibility': 'hidden'});

    // Hide the svg box and the text
    let box = $('#value-box');
    box.attr('x', 0);
    box.attr('y', 0);
    box.attr('height', 0);
    box.attr('width', 0);
    box.css('visibility', 'hidden');

    let roomText = $('#room-title-text');
    let valueText = $('#room-value-text');

    roomText.html("");
    valueText.html("");
    roomText.css('visibility', 'hidden');
    valueText.css('visibility', 'hidden');
}

function startSVGUpdating() {
    let secInterval = setInterval(() => {
        if (new Date().getSeconds() === 0) {
            clearInterval(secInterval);
            let minInterval = setInterval(() => {
                if (new Date().getMinutes() % 5 === 0) {
                    clearInterval(minInterval);
                    setInterval(loadSvg, 5 * 60 * 1000); // Reload every 5 minutes
                    loadSvg();
                }
            }, 60 * 1000);
        }

    }, 1000);
}

function toggleDisplay() {
    isShowingTemperature = !isShowingTemperature;
    loadSvg();
}

$(document).ready(() => {
    loadSvg();

    setTimeout(startSVGUpdating(), 100); //Detach a loop into a thread
});