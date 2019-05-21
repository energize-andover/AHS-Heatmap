$('.navbar-burger').first().click(() => {
    $('.navbar-burger').first().toggleClass('is-active');
    $('#sidenav').toggleClass('active');
});

$('.sidenav-dropdown-title').each((indx, title) => {
    let dropdown = $(title).parent();
    let hidden = dropdown.children('.sidenav-dropdown-hidden').first();

    dropdown.mouseenter(() => {
        hidden.slideDown();
    });
    dropdown.mouseleave(() => {
        hidden.slideUp();
    });
});