$(document).ready(function() {
    getLikes()
        // note - need to find from model whether heart button is liked by current user then can call like functions together


    // toggles colour of heart button is liked/hearted
    alertId();
    $('.heartButton').click(function() {
        var id = event.target.id;
        var post = document.getElementById(id);
        var src = post.getAttribute('src');


        var unliked = "/static/images/heart2.png";
        var liked = "/static/images/hearted.png";

        if (src == unliked) {
            post.setAttribute('src', liked);
            alert("liked");
        } else {
            post.setAttribute('src', unliked);
            alert("unliked");
        }
    });


    // increase like of post 
    $('.heartButton').click(function() {
        var id = event.target.id;
        var post = document.getElementById(id);
        var postId = post.getAttribute('id');

        $.get('/feed/show_post/${postId}/like-post/',
            function(data) {
                post.html(data);
            }
        )

    });


    adjustColumns();


    $(window).resize(function() {
        adjustColumns();
    })



})


function alertId() {
    //alert(user_id)
}


// currently just prints out alert of estimated no. columns
function adjustColumns() {
    var pictureWidth = 460; // may need to be adjusted
    var windowWidth = $(window).width();

    if (windowWidth < pictureWidth) {
        //alert('1 column needed');
    } else if (windowWidth < pictureWidth * 2) {
        //alert ('2 columns needed');
    } else if (windowWidth < pictureWidth * 3) {
        //alert ('3 columns needed');
    } else if (windowWidth < pictureWidth * 4) {
        //alert ('4 columns needed');
    } else if (windowWidth < pictureWidth * 5) {
        //alert ('5 columns needed');
    }
}
const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const getLikes = function() {
    $.ajax({
        type: 'POST',
        url: urlConstruct,
        data: {
            'csrfmiddlewaretoken': csrf,
            'user': user_id,

        },
        success: (res) => {
            setLikes(res)
        },
        error: (err) => {
            console.log(err)
        }


    })
}

const setLikes = function(result) {
    console.log("setting likes")

    //var unliked = "/static/images/heart2.png";
    var liked = "/static/images/hearted.png"
    console.log(result)
    for (let i = 0; i < result["data"].length; i++) {
        console.log(i)
        var post = document.getElementById(result["data"][i]);

        post.setAttribute('src', liked);


    }
}