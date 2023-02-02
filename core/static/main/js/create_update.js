$('form').find('input,  select, textarea,number').each(function () {
    if($(this).attr('type') !== 'checkbox'){
        $(this).addClass('form-control');
    }

    if($(this).attr('col')){
        if($(this).attr('type') == 'checkbox'){
            $(this).parent().parent().parent().addClass($(this).attr('col'));
            $(this).parent().parent().parent().addClass('pt-5 pl-3');
        }else{
            $(this).parent().parent().parent().addClass($(this).attr('col'));
        }
    }
});

