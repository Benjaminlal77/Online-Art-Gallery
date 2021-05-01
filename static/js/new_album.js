window.onload=function(){
    var spaceless_inputs = document.querySelectorAll('.spaceless-input')
    
    spaceless_inputs.forEach(spaceless_input => {
        spaceless_input.addEventListener('input', function(event){
            spaceless_input.value = spaceless_input.value.replace(/\s+/g, '_');
        });
    });
};