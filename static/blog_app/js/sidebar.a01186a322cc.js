let recentButton = document.getElementById("recent");
let popularButton = document.getElementById("popular");
let recentPosts = document.getElementsByClassName('recent');
let popularPosts = document.getElementsByClassName('popular');
recentButton.onclick = () => {
    recentButton.classList.remove('btn-secondary');
    recentButton.classList.add('btn-primary');
    popularButton.classList.add('btn-secondary');
    popularButton.classList.remove('btn-primary');
    for (let i = 0; i < recentPosts.length; i++) {
        recentPosts[i].style.display = 'block';
       
    };
    for (let i = 0; i < popularPosts.length; i++) {
        popularPosts[i].style.display = 'none'
    };

};

popularButton.onclick = () => {
    popularButton.classList.remove('btn-secondary');
    popularButton.classList.add('btn-primary');
    recentButton.classList.add('btn-secondary');
    recentButton.classList.remove('btn-primary');
    for (let i = 0; i < recentPosts.length; i++) {
        recentPosts[i].style.display = 'none'
    };
    for (let i = 0; i < popularPosts.length; i++) {
        popularPosts[i].style.display = 'block'
    };
};