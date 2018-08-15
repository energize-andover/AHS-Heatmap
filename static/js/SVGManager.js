function sleep(ms) {

    return new Promise(resolve => setTimeout(resolve, ms));
}

async function load_svg() {
    $("#svg-obj").css('display', 'none');
    $("#svg").load("index.html #svg-obj");
    await sleep(1000);
    let svg = document.getElementById('svg').firstChild;
    svg.setAttribute('data', '../static/svg/Andover%20HS%20level%203.svg');
    svg.setAttribute('width', 'auto');
    svg.setAttribute('height', 'auto');
    svg.setAttribute('opacity', '1');
    svg.setAttribute('visibility', 'visible');

    await sleep(1000);

    $(svg).css('display', 'block');

    let viewBox = svg.getSVGDocument().childNodes[2].getAttribute('viewBox');
    let viewBoxDimensions = viewBox.split(' ');
    let maxTries = 3;

    tryViewBox(maxTries, viewBoxDimensions);
    init(maxTries);
    
    getAllData(2);

    let rooms = getRooms();
}