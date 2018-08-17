function sleep(ms) {

    return new Promise(resolve => setTimeout(resolve, ms));
}

async function start_script() {
    await sleep(2000);
    let svg = document.getElementById('svg-obj').getSVGDocument().getElementsByTagName('svg')[0];
    await sleep(1000);

    let viewBox = svg.getAttribute('viewBox');
    let viewBoxDimensions = viewBox.split(' ');

    let svg_width = viewBoxDimensions[2];
    let svg_height = viewBoxDimensions[3];

    let maxTries = 3;

    tryViewBox(maxTries, viewBoxDimensions);
    init(maxTries);

    getAllData(2);

    let rooms = getRooms();

    rooms.forEach((room) => {
        // [[topLeftX, topLeftY, bottomLeftX, bottomLeftY, bottomLeftX, bottomLeftY, topRightX, topRightY] (All as a % of the width or height), color (Do it later), temperature, units]
        getRoomInfo(room);
        let roomInfo = getCurrentRoomInfo();

        if (roomInfo.length !== 0) {
            //<path d="M 100 100 L 300 100 L 300 300 L 100 300 Z" stroke="green" stroke-width="3" fill="green" />
            let coords = roomInfo[0];

            let path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.setAttributeNS(null, "d", `M ${Math.round(coords[0] * svg_width)} ${Math.round(coords[1] * svg_height)} L ${Math.round(coords[2] * svg_width)} ${Math.round(coords[3] * svg_height)} L ${Math.round(coords[4] * svg_width)} ${Math.round(coords[5] * svg_height)} L ${Math.round(coords[6] * svg_width)} ${Math.round(coords[7] * svg_height)} Z`);
            path.setAttributeNS(null, "stroke", "green");
            path.setAttributeNS(null, "stroke-width", "3");
            path.setAttributeNS(null, "fill", "green");

            svg.appendChild(path);
        }
    })
}