function showRoomData(path, oldValue, oldUnits) {
    let roomText = $('#room-title-text');
    let valueText = $('#room-value-text');

    if (window.location.href.includes("/ahs/3") || window.location.href.includes("/ahs/4")) {
        roomText.css('font-size', '150px');
        valueText.css('font-size', '150px');
    }

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
    let textPadding = 20;

    // Move text and fill in with value
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
    valueText.html(`${isShowingTemperature ? 'Temperature' : 'CO2 Level'}: ${oldValue}${oldUnits.replace('deg ', '&#176;')}`);

    // Move and show the svg box
    let box = $('#value-box');
    let boxCoords = [valueTextCoords[0] - boxPadding / 4, roomTextCoords[1] - roomTextBBox.height - textPadding / 2];

    let view_box = $('#svg-container').children('svg').first().attr('viewBox').split(' ');

    let box_height = 4 * textPadding + roomTextBBox.height + document.getElementById('room-value-text').getBBox().height;
    let box_width = 3 * boxPadding / 4 + document.getElementById('room-value-text').getBBox().width;
    let box_x = boxCoords[0], box_y = boxCoords[1];

    if (box_x + box_width >= view_box[2]) {
        // The box would extend outside of the viewBox
        box_x -= box_width + getRoomPathWidth(path) + 3 * cornerPadding; // Move the box so that one of its RIGHT corners is at (box_x, box_y)
        roomText.attr('x', roomTextCoords[0] - box_width - getRoomPathWidth(path) - 3 * cornerPadding);
        valueText.attr('x', valueTextCoords[0] - box_width - getRoomPathWidth(path) - 3 * cornerPadding);
    }

    if (box_y + box_height >= view_box[3]) {
        // The box would extend outside of the viewBox
        box_y -= box_height + getRoomPathHeight(path) + 3 * cornerPadding; // Move the box and text to stay on screen and not cover
        roomText.attr('y', roomTextCoords[1] - box_height - getRoomPathHeight(path) - 3 * cornerPadding);
        valueText.attr('y', valueTextCoords[1] - box_height - getRoomPathHeight(path) - 3 * cornerPadding);
    }

    box.attr('x', box_x);
    box.attr('y', box_y);
    box.attr('height', box_height);
    box.attr('width', box_width);
    box.css('fill', 'white');
    box.css('stroke', 'black');
    box.css('stroke-width', '4');
    box.css('visibility', 'visible');
}

function getRoomPathWidth(path) {
    let pathD = $(path).attr('d');
    let split = pathD.split('L');
    // To get width:
    // split[2] up to first space - split[1] up to first space
    let svg_width = Math.abs(parseFloat(split[1].split(' ')[0]) - parseFloat(split[2].split(' ')[0]));

    // Calculate pixel width based on SVG width
    let svg = $(path).parents('svg').first().parent('svg').first();
    let viewBox = $(svg).attr('viewBox').split(' ');
    let width = $(svg).width();

    return svg_width / viewBox[2] * width;
}

function getRoomPathHeight(path) {
    let pathD = $(path).attr('d');
    let split = pathD.split('L');
    // To get height:
    // split[1] between first and second space - split[0] between first and second space
    let svg_height = Math.abs(parseFloat(split[1].split(' ')[1]) - parseFloat(split[0].split(' ')[1]));

    // Calculate pixel width based on SVG width
    let svg = $(path).parents('svg').first().parent('svg').first();
    let viewBox = $(svg).attr('viewBox').split(' ');
    let height = $(svg).height();

    return svg_height / viewBox[3] * height;
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