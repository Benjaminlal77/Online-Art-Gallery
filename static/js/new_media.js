window.onload=function(){
    var file_input = document.getElementById('file-input');
    var spaceless_inputs = document.querySelectorAll('.spaceless-input')

    file_input.addEventListener('input', function(event){
        event.preventDefault();
        let file_label = document.getElementById('file-label');
        let files = file_input.files;
        let file_names = "";

        for (i=0; i<files.length; i++){
            let file = files[i];
            file_names = file_names + file.name + ", ";
        };
        file_label.innerHTML = file_names;
    });
    
    spaceless_inputs.forEach(spaceless_input => {
        spaceless_input.addEventListener('input', function(event){
            spaceless_input.value = spaceless_input.value.replace(/\s+/g, '_');
        });
    });
};
