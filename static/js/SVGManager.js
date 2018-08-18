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
       fillRoom(room);
    });
}