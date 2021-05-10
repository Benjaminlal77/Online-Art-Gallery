window.onload=function(){
    var password1 = document.getElementById('id_password1');
    var password2 = document.getElementById('id_password2');
    
    password1.addEventListener('change',function(event){
        event.preventDefault();
        if (password1.value.length < 8 || password1.value.length > 150){
            password1.style.borderColor = 'rgb(220, 53, 69)';
        } else {
            password1.style.borderColor = 'rgb(49, 171, 77)';
        };
    });
    password2.addEventListener('change',function(event){
        event.preventDefault();
        if (password2.value === password1.value){
            password2.style.borderColor = 'rgb(49, 171, 77)';
        } else{
            password2.style.borderColor = 'rgb(220, 53, 69)'
        }
    });
};