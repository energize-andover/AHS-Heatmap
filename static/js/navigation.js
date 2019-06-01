let overlay = $("#overlay");

function hideOverlay() {
    overlay.css('opacity', '0');
    setTimeout(() => {
        overlay.css('visibility', 'hidden'); // Make sure the animation finishes before making it invisible
    }, 500);
}

$('.navbar-burger').first().click(() => {
    $('.navbar-burger').first().toggleClass('is-active');

    let sidenav = $('#sidenav');

    sidenav.toggleClass('active');

    if (sidenav.hasClass('active')) {
        // Sidenav is opening
        overlay.css('visibility', 'visible');
        overlay.css('opacity', '0.6');
    } else {
        // Sidenav is closing
        hideOverlay();
    }
});

overlay.click(() => {
    $("#sidenav").removeClass('active');
    $('.navbar-burger').first().removeClass('is-active');
    hideOverlay();
});

/** Detect mobile browsers using mobile-detect.js (https://github.com/hgoebl/mobile-detect.js) **/
let md = new MobileDetect(window.navigator.userAgent);

function adjustNav() {
    $('.sidenav-dropdown-title').each((indx, title) => {
        let dropdown = $(title).parent();
        let hidden = dropdown.children('.sidenav-dropdown-hidden').first();

        if (md.mobile() == null) {
            dropdown.mouseenter(() => {
                hidden.slideDown();
                $(title).children('.dropdown-caret').css('transform', 'rotate(0deg)');
            });
            dropdown.mouseleave(() => {
                hidden.slideUp();
                $(title).children('.dropdown-caret').css('transform', '');
            });
        } else {
            hidden.css('display', 'block !important');
        }
    });
}

adjustNav();

$(window).resize(() => {
    adjustNav();
});


// Keep dropdown expanded if active page is part of it
let activeLink = $('.active-page').first();
if (activeLink.hasClass('sidenav-dropdown-item')) {
    dropdown = activeLink.parents('.sidenav-dropdown-hidden').each((indx, hidden) => {
        $(hidden).addClass('hidden-revealed');
    });
}

// Add FontAwesome caret icons to each dropdown title
$('.sidenav-dropdown-title').each((indx, titleDOM) => {
    let title = $(titleDOM);

    title.append('<i class="fas fa-caret-up dropdown-caret"></i>'); // Add the caret icon
});