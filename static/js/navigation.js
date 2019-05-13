$('.navbar-burger').first().click(() => {
    $('.navbar-burger').first().toggleClass('is-active');
    $('#sidenav').toggleClass('active');
});