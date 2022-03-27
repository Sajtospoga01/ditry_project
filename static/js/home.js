$(document).ready(function() {
    if (urlConstruct != undefined) {
        getLikeStatus()
    }

    // note - need to find from model whether heart button is liked by current user then can call like functions together




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





})

// currently just prints out alert of estimated no. columns

const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const getLikeStatus = function() {
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
        if (post != null) {
            post.setAttribute('src', liked);
        }



    }
}