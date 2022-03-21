$(document).ready(function() {
	

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


