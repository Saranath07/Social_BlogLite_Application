function validate(event){
    const email = document.querySelector("#email").value;
    if(email.indexOf("@") == -1){
        event.preventDefault();
        alert("Enter a valid email");
        return false;
    }
    return true;



}


function send_like(event){
    
    
    article = event.target
    
    article_id = article.dataset.article_id;
    
    fetch("/like/"+article_id).then(
        response => response
    ).catch(
        err => alert(err)
    )
    
    
   
        let counter = localStorage.getItem(`#like${article_id}`);
        
        counter++;
        console.log(counter)
        document.querySelector(`#like${article_id}`).innerHTML = ` ${counter}`;
        localStorage.setItem(`#like${article_id}`, counter);
        
        // console.log(like_button.dataset.article_likes)
        
        
    }


function initialize(){
    like_buttons = document.querySelectorAll(".like-icon");
    
    for(const like_button of like_buttons){
        localStorage.setItem(`#like${like_button.dataset.article_id}`, like_button.dataset.article_likes);
        
        // console.log(like_button.dataset.article_likes)
        like_button.onclick = send_like;
        
    }
    
}

function send_like_comment(event){
    
    
    comment = event.target
    
    comment_id = comment.dataset.comment_id;
    
    fetch("/comment_like/"+comment_id).then(
        response => response
    ).catch(
        err => alert(err)
    )
    
    
   
        let counter = localStorage.getItem(`#c_like${comment_id}`);
        
        counter++;
        console.log(counter)
        document.querySelector(`#c_like${comment_id}`).innerHTML = ` ${counter}`;
        localStorage.setItem(`#c_like${comment_id}`, counter);
        
        // console.log(like_button.dataset.comment_likes)
        
        
    }


function initialize1(){
    like_buttons = document.querySelectorAll(".clike-icon");
    
    for(const like_button of like_buttons){
        localStorage.setItem(`#c_like${like_button.dataset.comment_id}`, like_button.dataset.comment_likes);
        
        // console.log(like_button.dataset.comment_likes)
        like_button.onclick = send_like_comment;
        
    }
    
}