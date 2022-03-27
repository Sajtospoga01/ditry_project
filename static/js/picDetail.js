$(document).ready(function() {
    getFollowStatus();
})


const getFollowStatus = function() {
    $.ajax({
        type: 'POST',
        url: urlConstructFollow,
        data: {
            'csrfmiddlewaretoken': csrf,
            'user': user_id,
            'other_user': user_2_id,

        },
        success: (res) => {
            console.log(res)
            setFollow(res)

        },
        error: (err) => {
            console.log(err)
        }


    })
}

const setFollow = function(result) {
    var isFollowed = result["followed"]
    console.log(isFollowed)
    var element = document.getElementById("follow");
    console.log(element)
    if (element != null && isFollowed) {

        element.innerText = "Following"
    }
}