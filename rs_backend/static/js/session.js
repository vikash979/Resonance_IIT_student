$(window).on('load',function(){
    $('#session_page').addClass("active");
    ///////////////////////years appended
    var d = new Date();
    var n = d.getFullYear(n)
    var i =2015;
    for (var i =2015;i<=n;i++)
    {
    
    $('#year').append(`<option value="${i}" selected="selected">${i}</option>`);
    $('#years').append(`<option value="${i}" selected="selected">${i}</option>`);
    }
////////////////////////////Program list in session
   $.ajax({
    url: BASE_SITE_URL + '/api/v1/institute/program/',
    type: "POST",
    dataType: "json",
    data:{"action":"view"},
    success: function(response){
        if (response.status==true)
        {
            let lineNo = 1;
            tableBody = $("table tbody");
            let tableData = JSON.stringify(response.data)
            for(var i=0;i<response.data.length;i++){
                $('#program_id').append(`<option value="${response.data[i].id}" selected="selected">${response.data[i].display_name}</option>`);
                $('#programs_ids').append(`<option value="${response.data[i].id}" selected="selected">${response.data[i].display_name}</option>`);
           
            
            }
            // alert(length(tableData))
        }
        
    }
    })
   /////////////////////////////////list of session///////////////
    session_paging()
})
function session_paging(sessionCount)
{
    if (sessionCount== undefined)
    {
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/sessions/',
            type: "POST",
            dataType: "json",
            data:{"action":"view"},
            success: function(response){
                $('#total_session').text(response.data.length)
                //alert(JSON.stringify(response.data))
                $('#listingtable').html('')
                    $('#pagination').html('')
                if (response.data.length > 0)
                {
                    for(var i=0;i<response.data.length;i++){
                    $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                    }

                }
                else{
                    $('#listingtable').append(`<tr> <td colspan="4">There is no record</td></tr>`)
                }

                var pagi_length =response.paginations['session_numpage']+1
                     
                if (response.paginations['session_numpage'] > 0){
                    if(response.paginations['session_user_changes']==true)
                    {
                       if(response.paginations['session_previous']==true){

                        $('#pagination').append(`<a href="#" onclick="session_paging(${response.paginations['session_previous_page']})">prev</a>`)
                           
                       }
                       // else{
                       //     $('#pagination').append(`<span>&laquo;</span>`)
                       // }
                       for (var i=1;i<pagi_length;i++)
                       {
                        if (response.paginations['current_page']==i)
                        {
                            
                           $('#pagination').append(`<a href="#" class="selected">${i}</a>`)
                        }  
                        else{
                            
                           $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="session_paging(${i});">${i}</a>`)
                        }
                       }
                       if (response.paginations['session_next']==true)
                       {
                           $('#pagination').append(`<a href="#" onclick="session_paging(${response.paginations['session_next_page_number']});">next</a>`)
                       }
                       
                    }
                    //location.reload();
                }
            }
        })
    }
    else{
        $.ajax({
            url: BASE_SITE_URL + '/api/v1/institute/sessions/',
            type: "POST",
            dataType: "json",
            data:{"action":"view","page":sessionCount},
            success: function(response){
                $('#total_session').text(response.data.length)
                //alert(JSON.stringify(response.data))
                if (response.data.length > 0)
                {
                    $('#listingtable').html('')
                    $('#pagination').html('')
                    for(var i=0;i<response.data.length;i++){
                    $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                    }
                    var pagi_length =response.paginations['session_numpage']+1
                     
                    if (response.paginations['session_numpage'] > 0){
                        if(response.paginations['session_user_changes']==true)
                        {
                           if(response.paginations['session_previous']==true){
    
                            $('#pagination').append(`<a href="#" onclick="session_paging(${response.paginations['session_previous_page']})">prev</a>`)
                               
                           }
                           // else{
                           //     $('#pagination').append(`<span>&laquo;</span>`)
                           // }
                           for (var i=1;i<pagi_length;i++)
                           {
                            if (response.paginations['current_page']==i)
                            {
                                
                               $('#pagination').append(`<a href="#" class="selected">${i}</a>`)
                            }  
                            else{
                                
                               $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="session_paging(${i});">${i}</a>`)
                            }
                           }
                           if (response.paginations['session_next']==true)
                           {
                               $('#pagination').append(`<a href="#" onclick="session_paging(${response.paginations['session_next_page_number']});">next</a>`)
                           }
                           
                        }
                        //location.reload();
                    }
                }
                else{
                    $('#listingtable').append(`<tr> <td colspan="4">There is no record</td></tr>`)
                }
            }
        })
    }
}
    $( "#year" ).change(function() {
        var id = $(this).id
        
      });

      //////////////////////////////////////show records in edit file//////////////////////


function editClass(attrId)

{
    
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/sessions/',
        type: "POST",
        dataType: "json",
        data:{"action":"view","id":attrId},
        success: function(response){
            if (response.status ==true){
                 var display_name = $('#display_names').val(response.data[0]['display_name'])
                 var names = $('#names').val(response.data[0]['name'])
                 var descriptions = $('#descriptions').val(response.data[0]['description'])
                //  var description = $('#desc').val(response.data[0]['description'])
                var hidden_id = $('#hidden_class_id').val(attrId)
              
               
            }
            else{
                var class_saved = "Failed"
            }
        }
    })
    jQuery('.addDivisionDialog.foredit').addClass('open');
}
///////////////////////////add session //////////////////
 $("#add_session").click( function(e){
    var display_name = $('#display_name').val()
    var description = $('#description').val()
    var name = $('#name').val()
    var year = $('#year').val()
    var program = $('#program_id').val()
    
    for (var i=0;i<program.length;i++)
    {
        var programs = program[i]
    
   
   dataString = {"action":"add","display_name":display_name,"description":description,"name":name,"year":year,"program":programs}
   
    
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/sessions/',
        type: "POST",
        dataType: "json",
        data:dataString,
        success: function(response){
            if (response.status ==true){
                var class_saved = "Success Fully Saved"
                var display_name = $('#display_name').val(' ')
                var description = $('#description').val(' ')
                var name = $('#name').val(' ')
                var year = $('#year').val(' ')
                var program = $('#program_id').val(' ')
                jQuery('.addDivisionDialog.foredit').removeClass('open');
                location.reload();

            }
            else{
                var class_saved = "Failed"
            }
        }

   })
}

 })

/////////////////////////Update///////////
$("#edit_session").click( function(e){
    var display_name = $('#display_names').val()
    var description = $('#descriptions').val()
    var name = $('#names').val()
    var year = $('#years').val()
    var program = $('#programs_ids').val()
    var hidden_id = $('#hidden_class_id').val()
   
    dataString = {"action":"Update","display_name":display_name,"description":description,"name":name,"year":year,"program":program,"id":hidden_id}
    
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/sessions/',
        type: "POST",
        dataType: "json",
        data:dataString,
        success: function(response){
            if (response.status ==true){
                location.reload();
                // var class_saved = "Success Fully Saved"
                // var display_name = $('#display_name').val(' ')
                // var description = $('#description').val(' ')
                // var name = $('#name').val(' ')
                // var year = $('#year').val(' ')
                // var program = $('#program_id').val(' ')
                // jQuery('.addDivisionDialog.foredit').removeClass('open');
                // location.reload();

            }
            else{
                var class_saved = "Failed"
            }
        }

   })

 })

 /////////////////Remover

 function remove(removeid)
{
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/sessions/',
        type: "POST",
        dataType: "json",
        data:{"action":"remove","id":removeid},
        success: function(response){
            if (response.status ==true){
                var class_saved = "Success Fully Saved"
                
                location.reload();

            }
            else{
                var class_saved = "Failed"
            }
        }

   })
}


//////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
///////////////////////////////////////////////////
$(' aside .aside-container li.active').addClass('open').children('ul').show();
$('aside .aside-container li.has-sub>a').on('click', function(){
    //$(this).removeAttr('href');
    var element = $(this).parent('li');
    if (element.hasClass('open')) {
        element.removeClass('open');
        element.find('li').removeClass('open');
        element.find('ul').slideUp(200);
    }
    else {
        element.addClass('open')
        element.children('ul').slideDown(200);
        element.siblings('li').children('ul').slideUp(200);
        element.siblings('li').removeClass('open');
        element.siblings('li').find('li').removeClass('open');
        element.siblings('li').find('ul').slideUp(200);
    }
});

 $("#upload_link").on('click', function(e){
    e.preventDefault();
    $("#upload:hidden").trigger('click');
})

let tableData = [
    // { id: '1', concepttitle: 'Electrostatic force', studenttitle: 'Physics'},
    // { id: '2', concepttitle: 'Linear equations', studenttitle: 'Mathematics'},
    // { id: '3', concepttitle: 'Thermodynamics', studenttitle: 'Chemistry'},
    // { id: '4', concepttitle: 'Laws of motion', studenttitle: 'Physics'},
    // { id: '5', concepttitle: 'Algebra', studenttitle: 'Mathematics'},
  
    
]


// let paginationData = [
//     { id: '1', concepttitle: 'Electrostatic force', studenttitle: 'Physics'},
//     { id: '2', concepttitle: 'Linear equations', studenttitle: 'Mathematics'},
//     { id: '3', concepttitle: 'Thermodynamics', studenttitle: 'Chemistry'},
//     { id: '4', concepttitle: 'Laws of motion', studenttitle: 'Physics'},
//     { id: '5', concepttitle: 'Algebra', studenttitle: 'Mathematics'},
// ]


     function confirmation(type){
         if (type === 'confirm'){
            console.log("confirm");
         }else{
           console.log("cancel"); 
         }  
    }

    function success(type){
         if (type === 'ok'){
            console.log("ok");
         }else{
           console.log("cancel"); 
         }  
    }


jQuery(document).ready(function(){




let tableHTML ='';
let paginationHTML ='';


tableData.forEach((val)=>{
    tableHTML += `<tr>
               <td>${val.concepttitle}</td>
               <td>${val.studenttitle}</td>
               <td><a href="javascript:void(0);" class='edit-link'><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a></td>
            </tr>`;

            
});


jQuery('.listingtable').append(tableHTML);





jQuery('#txt-search').keyup(function(e){
    let searchValue = $(this).val().toLowerCase();
         console.log(searchValue);
         console.log(tableData);
         let getData = tableData.find(data => data.name === searchValue);
         console.log(getData);

    });


jQuery('.add-division-link').click(function(){
    //jQuery('.filter-section').css('display','flex');
    jQuery('.addDivisionDialog').addClass('open');
    jQuery('.addDivisionDialog.foredit').removeClass('open');

});  

jQuery('table td .edit-link').click(function(){
    //jQuery('.filter-section').css('display','flex');
    jQuery('.addDivisionDialog.foredit').addClass('open');
    

});  

$('#subjectdd, #editsubjectdd').selectpicker(); 

jQuery('.addDivisionDialog .form-actions a').click(function(){
    jQuery('.addDivisionDialog').removeClass('open');
});
jQuery('.addDivisionDialog .form-actions a').click(function(){
    jQuery('.addDivisionDialog.foredit').removeClass('open');
});



});









$( "form" ).on( "submit", function( event ) {
  event.preventDefault();
  console.log( $( this ).serializeArray() );
});

var input = document.querySelector('input[name="input-custom-dropdown"]'),
// init Tagify script on the above inputs
tagify = new Tagify(input, {
whitelist: ["A# .NET", "A# (Axiom)", "A-0 System", "A+", "A++", "ABAP", "ABC", "ABC ALGOL", "ABSET", "ABSYS", "ACC", "Accent", "Ace DASL", "ACL2", "Avicsoft", "ACT-III", "Action!", "ActionScript", "Ada", "Adenine", "Agda", "Agilent VEE", "Agora", "AIMMS", "Alef", "ALF", "ALGOL 58", "ALGOL 60", "ALGOL 68", "ALGOL W", "Alice", "Alma-0", "AmbientTalk", "Amiga E", "AMOS", "AMPL", "Apex (Salesforce.com)", "APL", "AppleScript", "Arc", "ARexx", "Argus", "AspectJ", "Assembly language", "ATS", "Ateji PX", "AutoHotkey", "Autocoder", "AutoIt", "AutoLISP / Visual LISP", "Averest", "AWK", "Axum", "Active Server Pages", "ASP.NET", "B", "Babbage", "Bash", "BASIC", "bc", "BCPL", "BeanShell", "Batch (Windows/Dos)", "Bertrand", "BETA", "Bigwig", "Bistro", "BitC", "BLISS", "Blockly", "BlooP", "Blue", "Boo", "Boomerang", "Bourne shell (including bash and ksh)", "BREW", "BPEL", "B", "C--", "C++ – ISO/IEC 14882", "C# – ISO/IEC 23270", "C/AL", "Caché ObjectScript", "C Shell", "Caml", "Cayenne", "CDuce", "Cecil", "Cesil", "Céu", "Ceylon", "CFEngine", "CFML", "Cg", "Ch", "Chapel", "Charity", "Charm", "Chef", "CHILL", "CHIP-8", "chomski", "ChucK", "CICS", "Cilk", "Citrine (programming language)", "CL (IBM)", "Claire", "Clarion", "Clean", "Clipper", "CLIPS", "CLIST", "Clojure", "CLU", "CMS-2", "COBOL – ISO/IEC 1989", "CobolScript – COBOL Scripting language", "Cobra", "CODE", "CoffeeScript", "ColdFusion", "COMAL", "Combined Programming Language (CPL)", "COMIT", "Common Intermediate Language (CIL)", "Common Lisp (also known as CL)", "COMPASS", "Component Pascal", "Constraint Handling Rules (CHR)", "COMTRAN", "Converge", "Cool", "Coq", "Coral 66", "Corn", "CorVision", "COWSEL", "CPL", "CPL", "Cryptol", "csh", "Csound", "CSP", "CUDA", "Curl", "Curry", "Cybil", "Cyclone", "Cython", "Java", "Javascript", "M2001", "M4", "M#", "Machine code", "MAD (Michigan Algorithm Decoder)", "MAD/I", "Magik", "Magma", "make", "Maple", "MAPPER now part of BIS", "MARK-IV now VISION:BUILDER", "Mary", "MASM Microsoft Assembly x86", "MATH-MATIC", "Mathematica", "MATLAB", "Maxima (see also Macsyma)", "Max (Max Msp – Graphical Programming Environment)", "Maya (MEL)", "MDL", "Mercury", "Mesa", "Metafont", "Microcode", "MicroScript", "MIIS", "Milk (programming language)", "MIMIC", "Mirah", "Miranda", "MIVA Script", "ML", "Model 204", "Modelica", "Modula", "Modula-2", "Modula-3", "Mohol", "MOO", "Mortran", "Mouse", "MPD", "Mathcad", "MSIL – deprecated name for CIL", "MSL", "MUMPS", "Mystic Programming L"],
maxTags: 10,
dropdown: {
maxItems: 20,           // <- mixumum allowed rendered suggestions
classname: "tags-look", // <- custom classname for this dropdown, so it could be targeted
enabled: 0,             // <- show suggestions on focus
closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
}
}) 



$( "form" ).on( "submit", function( event ) {
    event.preventDefault();
    console.log( $( this ).serializeArray() );
  });

var input = document.querySelector('input[name="input-custom-dropdown"]'),
// init Tagify script on the above inputs
tagify = new Tagify(input, {
whitelist: ["A# .NET", "A# (Axiom)", "A-0 System", "A+", "A++", "ABAP", "ABC", "ABC ALGOL", "ABSET", "ABSYS", "ACC", "Accent", "Ace DASL", "ACL2", "Avicsoft", "ACT-III", "Action!", "ActionScript", "Ada", "Adenine", "Agda", "Agilent VEE", "Agora", "AIMMS", "Alef", "ALF", "ALGOL 58", "ALGOL 60", "ALGOL 68", "ALGOL W", "Alice", "Alma-0", "AmbientTalk", "Amiga E", "AMOS", "AMPL", "Apex (Salesforce.com)", "APL", "AppleScript", "Arc", "ARexx", "Argus", "AspectJ", "Assembly language", "ATS", "Ateji PX", "AutoHotkey", "Autocoder", "AutoIt", "AutoLISP / Visual LISP", "Averest", "AWK", "Axum", "Active Server Pages", "ASP.NET", "B", "Babbage", "Bash", "BASIC", "bc", "BCPL", "BeanShell", "Batch (Windows/Dos)", "Bertrand", "BETA", "Bigwig", "Bistro", "BitC", "BLISS", "Blockly", "BlooP", "Blue", "Boo", "Boomerang", "Bourne shell (including bash and ksh)", "BREW", "BPEL", "B", "C--", "C++ – ISO/IEC 14882", "C# – ISO/IEC 23270", "C/AL", "Caché ObjectScript", "C Shell", "Caml", "Cayenne", "CDuce", "Cecil", "Cesil", "Céu", "Ceylon", "CFEngine", "CFML", "Cg", "Ch", "Chapel", "Charity", "Charm", "Chef", "CHILL", "CHIP-8", "chomski", "ChucK", "CICS", "Cilk", "Citrine (programming language)", "CL (IBM)", "Claire", "Clarion", "Clean", "Clipper", "CLIPS", "CLIST", "Clojure", "CLU", "CMS-2", "COBOL – ISO/IEC 1989", "CobolScript – COBOL Scripting language", "Cobra", "CODE", "CoffeeScript", "ColdFusion", "COMAL", "Combined Programming Language (CPL)", "COMIT", "Common Intermediate Language (CIL)", "Common Lisp (also known as CL)", "COMPASS", "Component Pascal", "Constraint Handling Rules (CHR)", "COMTRAN", "Converge", "Cool", "Coq", "Coral 66", "Corn", "CorVision", "COWSEL", "CPL", "CPL", "Cryptol", "csh", "Csound", "CSP", "CUDA", "Curl", "Curry", "Cybil", "Cyclone", "Cython", "Java", "Javascript", "M2001", "M4", "M#", "Machine code", "MAD (Michigan Algorithm Decoder)", "MAD/I", "Magik", "Magma", "make", "Maple", "MAPPER now part of BIS", "MARK-IV now VISION:BUILDER", "Mary", "MASM Microsoft Assembly x86", "MATH-MATIC", "Mathematica", "MATLAB", "Maxima (see also Macsyma)", "Max (Max Msp – Graphical Programming Environment)", "Maya (MEL)", "MDL", "Mercury", "Mesa", "Metafont", "Microcode", "MicroScript", "MIIS", "Milk (programming language)", "MIMIC", "Mirah", "Miranda", "MIVA Script", "ML", "Model 204", "Modelica", "Modula", "Modula-2", "Modula-3", "Mohol", "MOO", "Mortran", "Mouse", "MPD", "Mathcad", "MSIL – deprecated name for CIL", "MSL", "MUMPS", "Mystic Programming L"],
maxTags: 10,
dropdown: {
  maxItems: 20,           // <- mixumum allowed rendered suggestions
  classname: "tags-look", // <- custom classname for this dropdown, so it could be targeted
  enabled: 0,             // <- show suggestions on focus
  closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
}
}) 


