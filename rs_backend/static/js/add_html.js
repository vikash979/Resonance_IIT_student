$.fn.serializeObject = function(){
  jQuery.ajaxSettings.traditional = true;
  var obj = {};
  $.each( this.serializeArray(), function(i,o){
    var n = o.name,
        v = o.value;
        obj[n] = obj[n] === undefined ? v
          : $.isArray( obj[n] ) ? obj[n].concat( v )
          : [ obj[n], v ];
  });
  return obj;
};

function clickError(){
  $('#error-dialogue').css("display","none");
  }

$(window).on('load',function(){
  $('#faculties_page').addClass("active");
  var department_count = 0;
  var conditions = {};
  var paginations = {};
  paginations.page = 0;
  var data = {};
  data.action="view";   
  data.conditions=JSON.stringify(conditions);
  data.paginations = JSON.stringify(paginations);
    $.ajax({
        url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
        type: "POST",
        dataType: "json",
        data:data,
        success: function(response){
          if (response.status != false) {
            for(var i=0;i<response.data.length;i++){
                $('#subject_list').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);    
              }  
              $('#subject_list').selectpicker('refresh');
            }
            else if (response.status == false) {
              $("#error-msg").html(response.error[0]+" !");
          $('#error-dialogue').css("display","flex");
          }
        },
        error: function(response){
          
          $("#error-msg").html("there is problem on serverside"+" !");
          $('#error-dialogue').css("display","none");
          $('#error-dialogue').css("display","flex");
      }
    });

  //   var department_count = 0;
  //   var conditions = {};
  //   var paginations = {};
  //   paginations.page = 0;
  //   var data = {};
  //   data.action="view";   
  //   data.conditions=JSON.stringify(conditions);
  //   data.paginations = JSON.stringify(paginations);

  //   $.ajax({
  //     url: BASE_SITE_URL + `/api/v1/institute/batches/`,
  //     type: "POST",
  //     dataType: "json",
  //     data:data,
  //     success: function(response){
  //         if (response.status != false) {
  //         for(var i=0;i<response.data.length;i++){
  //             $('#batches-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);          
  //         } 
  //         $('#batches-getting-started').selectpicker('refresh');  
  //       }
  //     }
  // });

  var department_count = 0;
  var conditions = {};
  var paginations = {};
  paginations.page = 0;
  var data = {};
  data.action="view";   
  data.conditions=JSON.stringify(conditions);
  data.paginations = JSON.stringify(paginations);

  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/division/`,
    type: "POST",
    dataType: "json",
    data:data,
    success: function(response){
        if (response.status != false) {
        for(var i=0;i<response.data.length;i++){
            $('#division-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].division}</option>`);          
        } 
        $('#division-getting-started').selectpicker('refresh');  
      }
      else if (response.status == false) {
       
        $("#error-msg").html(response.error[0]+" !");
    $('#error-dialogue').css("display","flex");
    }
    },
    error: function(response){
     
      $("#error-msg").html("there is problem on serverside"+" !");
      $('#error-dialogue').css("display","none");
      $('#error-dialogue').css("display","flex");
  }
});

var department_count = 0;
var conditions = {};
var paginations = {};
paginations.page = 0;
var data = {};
data.action="view";   
data.conditions=JSON.stringify(conditions);
data.paginations = JSON.stringify(paginations);

  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/designation/`,
    type: "POST",
    dataType: "json",
    data:data,
    success: function(response){
        if (response.status != false) {
        for(var i=0;i<response.data.length;i++){
          $('#designation-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].designation}</option>`);
          
        }
        $('#designation-getting-started').selectpicker('refresh');
      }
      else if (response.status == false) {
        $("#error-msg").html(response.error[0]+" !");
    $('#error-dialogue').css("display","flex");
    }
    },
    error: function(response){
      $("#error-msg").html("there is problem on serverside"+" !");
      $('#error-dialogue').css("display","none");
      $('#error-dialogue').css("display","flex");
  }
});

var department_count = 0;
var conditions = {};
var paginations = {};
paginations.page = 0;
var data = {};
data.action="view";   
data.conditions=JSON.stringify(conditions);
data.paginations = JSON.stringify(paginations);

  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/employement-type/`,
    type: "POST",
    dataType: "json",
    data:data,
    success: function(response){
      if (response.status != false) {
        for(var i=0;i<response.data.length;i++){
          $('#et-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].et_name}</option>`);
          
        }
        $('#et-getting-started').selectpicker('refresh'); 
    }
    else if (response.status == false) {
      $("#error-msg").html(response.error[0]+" !");
      $('#error-dialogue').css("display","flex");
  }
    },
    error: function(response){
      jQuery('#editEmployementDialog').removeClass('open');
      $("#error-msg").html("there is problem on serverside"+" !");
      $('#error-dialogue').css("display","none");
      $('#error-dialogue').css("display","flex");
  }
  });

  var department_count = 0;
  var conditions = {};
  var paginations = {};
  paginations.page = 0;
  var data = {};
  data.action="view";   
  data.conditions=JSON.stringify(conditions);
  data.paginations = JSON.stringify(paginations);

  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/department/`,
    type: "POST",
    dataType: "json",
    data:data,
    success: function(response){
        if (response.status != false) {
          
          for(var i=0;i<response.data.length;i++){
            $('#department-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].department}</option>`);
            
          }
          $('#department-getting-started').selectpicker('refresh'); 
          }
          else if (response.status == false) {
            $("#error-msg").html(response.error[0]+" !");
        $('#error-dialogue').css("display","flex");
        }
    },
    error: function(response){
      $("#error-msg").html("there is problem on serverside"+" !");
      $('#error-dialogue').css("display","none");
      $('#error-dialogue').css("display","flex");
  }
});

var department_count = 0;
var conditions = {};
var paginations = {};
paginations.page = 0;
var data = {};
data.action="view";   
data.conditions=JSON.stringify(conditions);
data.paginations = JSON.stringify(paginations);

$.ajax({
  url: BASE_SITE_URL + `/api/v1/auth/skill/`,
  type: "POST",
  dataType: "json",
  data:data,
  success: function(response){
      if (response.status != false) {
        
        for(var i=0;i<response.data.length;i++){
          $('#skill-getting-started').append(`<option value="${response.data[i].id}">${response.data[i].skill}</option>`);
          
        }
        $('#skill-getting-started').selectpicker('refresh'); 
        }
        else if (response.status == false) {
          $("#error-msg").html(response.error[0]+" !");
      $('#error-dialogue').css("display","flex");
      }
  },
  error: function(response){
    $("#error-msg").html("there is problem on serverside"+" !");
    $('#error-dialogue').css("display","none");
    $('#error-dialogue').css("display","flex");
}
});

});

// $(document).ready(function(){
//   var req_url = BASE_SITE_URL + `/api/v1/auth/country/`
//   $.ajax({
//     url: req_url,
//     type: 'GET',
//     success: function(response){
//       var country_input = $('select[name="Country"]');
//       for (var i=0;i<response.data.length;i++) {
//         country_input.append(`<option value='${response.data[i].country_name}'>${response.data[i].country_name}</option>`)
//       }
//     }
//   });
// });

$(document).ready(function(){

  
  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/country/`,
    type: 'GET',
    success: function(response){
      var country_input = $('select[name="Country"]');
      for (var i=0;i<response.data.length;i++) {
        country_input.append(`<option value='${response.data[i].id}'>${response.data[i].country_name}</option>`)
      }
      $('select[name="Country"]').selectpicker('refresh');
    },
    error: function(response){
      $("#error-msg").html("there is problem on serverside"+" !");
      $('#error-dialogue').css("display","none");
      $('#error-dialogue').css("display","flex");
  }
  });

  $.ajax({
      url: BASE_SITE_URL + `/api/v1/auth/roles/`,
      type: 'GET',
      success: function(response) {
        if (response.status != false) {
          for(var key in response.data){
            if (response.data.hasOwnProperty(key)) {
              var value = response.data[key];
              $('select[name="role"]').append(`<option value='${key}'>${value}</option>`)
            }
          }
        }
      }
    });

       

      $("#upload_link").on('click', function(e){
        e.preventDefault();
        $("#upload:hidden").trigger('click');
    }); 

    $('#subject_list').selectpicker(); 
    $('#batches-getting-started').selectpicker();
    $('#country-getting-started').selectpicker();  
    $('#center-getting-started').selectpicker();
    $('#region-getting-started').selectpicker();
    $('#state-getting-started').selectpicker();
    $('#city-getting-started').selectpicker();
    $('#division-getting-started').selectpicker();
    $('#designation-getting-started').selectpicker();
    $('#et-getting-started').selectpicker();
    $('#department-getting-started').selectpicker();

    // var input3 = document.querySelector('input[name="et"]'),
  
    // tagify = new Tagify(input3, {
    //   whitelist: et_list,
    //   maxTags: 10,
    //   dropdown: {
    //     maxItems: 20,           
    //     classname: "tags-look", 
    //     enabled: 0,             
    //     closeOnSelect: true    
    //   }
    // })

    // var input2 = document.querySelector('input[name="department"]'),
  
    // tagify = new Tagify(input2, {
    //   whitelist: department_list,
    //   maxTags: 10,
    //   dropdown: {
    //     maxItems: 20,           
    //     classname: "tags-look", 
    //     enabled: 0,             
    //     closeOnSelect: true    
    //   }
    // })

    // var input1 = document.querySelector('input[name="designation"]'),
    
    // tagify = new Tagify(input1, {
    //   whitelist: designation_list,
    //   maxTags: 10,
    //   dropdown: {
    //     maxItems: 20,           
    //     classname: "tags-look", 
    //     enabled: 0,             
    //     closeOnSelect: true    
    //   }
    // })

    // var input = document.querySelector('input[name="skill"]'),
   
    // tagify = new Tagify(input, {
    //   whitelist: skill_list,
    //   maxTags: 10,
    //   dropdown: {
    //     maxItems: 20,           
    //     classname: "tags-look", 
    //     enabled: 0,             
    //     closeOnSelect: false    
    //   }
    // })

    // var req_condition = new Object ;
    // function checkHtmlValues(tagtype){
    //   if(tagtype.prop("nodeName")=="SELECT"){
    //     req_condition[tagtype.attr("name")] = tagtype.val();
    //   }
    //   else if(tagtype.prop("nodeName")=="INPUT"){
    //     if(tagtype.attr("type")=="text"){
    //       if(tagtype.val().length!=0){
    //         if(tagtype.attr("data-type")=="input"){
    //           req_condition[tagtype.attr("name")] = tagtype.val();
    //         }
    //         else if(tagtype.attr("data-type")=="tagify"){
    //           req_tag = JSON.parse(tagtype.val());
    //           req_tag_list = new Array;
    //           for(var i=0;i<req_tag.length;i++){
    //             req_tag_list.push(req_tag[i]["value"]);
    //           }
    //           req_condition[tagtype.attr("name")] = req_tag_list;
    //         }
    //       }
    //     }
    //   }
      
    // }

    $("#faculty_creation").on('submit', function(e){
      e.preventDefault();
      // var value_conditions = new Object;
      // $('#faculty_creation').find('input,select').each(function(){
      //   checkHtmlValues($(this));
     
     req_data=$(this).serializeObject();
     data = new Object;
     data["action"]="create";
     data["data"]=JSON.stringify(req_data);
    //  console.log(JSON.stringify(data));
    console.log(data);
     $.ajax({
      url: BASE_SITE_URL + `/api/v1/auth/faculty/`,
      type: "POST",
      dataType: "json",
      data:data,
      success: function(response){
        if(response.status!=false){
          location.href = '/faculties/';
        }
        else if (response.status == false) {
          $("#error-msg").html(response.error[0]+" !");
      $('#error-dialogue').css("display","flex");
      }
      },
      error: function(response){
        $("#error-msg").html("there is problem on serverside"+" !");
        $('#error-dialogue').css("display","none");
        $('#error-dialogue').css("display","flex");
    }
    });
  });


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

    });


// });
// });

function regionlist(){
  if ($('select[name="Country"]').val() != "") {
    var country_val = $('select[name="Country"]').val();
    $.ajax({
      url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/`,
      type: 'GET',
      success: function(response){
        $('select[name="Region"]').empty();
        $('select[name="Region"]').append(`<option selected="selected" disabled>Select Region</option>`)
        $('select[name="Region"]').selectpicker('refresh');
        for (var i = 0; i < response.data.length; i++) {
            $('select[name="Region"]').append(`<option value='${response.data[i].id}'>${response.data[i].region_name}</option>`)

        }
        $('select[name="Region"]').selectpicker('refresh');
      }
    });
  }
}

function statelist(){
  if ($('select[name="Region"]').val() != ""){
    var country_val = $('select[name="Country"]').val();
    var region_val = $('select[name="Region"]').val();
    $.ajax({
      url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/${region_val}/`,
      type: 'GET',
      success: function(response){
        $('select[name="State"]').empty();
        $('select[name="State"]').append(`<option selected="selected" disabled>Select State</option>`)
        $('select[name="State"]').selectpicker('refresh');
        for (var i = 0; i < response.data.length; i++) {
          $('select[name="State"]').append(`<option value='${response.data[i].id}'>${response.data[i].state_name}</option>`)
        }
        $('select[name="State"]').selectpicker('refresh');
      }
    });
  }
}

function citylist(){
  if ($('select[name="State"]').val() != ""){
    var country_val = $('select[name="Country"]').val();
    var region_val = $('select[name="Region"]').val();
    var state_val = $('select[name="State"]').val();
    $.ajax({
      url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/${region_val}/${state_val}/`,
      type: 'GET',
      success: function(response){
        $('select[name="City"]').empty();
        $('select[name="City"]').append(`<option selected="selected" disabled>Select City</option>`)
        $('select[name="City"]').selectpicker('refresh');
        for (var i = 0; i < response.data.length; i++) {
          $('select[name="City"]').append(`<option value='${response.data[i].id}'>${response.data[i].city_name}</option>`)
        }
        $('select[name="City"]').selectpicker('refresh');
      }
    })
  }
}

function centerlist(){
  if ($('select[name="City"]').val() != ""){
    var country_val = $('select[name="Country"]').val();
    var region_val = $('select[name="Region"]').val();
    var state_val = $('select[name="State"]').val();
    var city_val = $('select[name="City"]').val();
    $.ajax({
      url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/${region_val}/${state_val}/${city_val}/`,
      type: 'GET',
      success: function(response){
        $('select[name="center"]').empty();
        $('select[name="center"]').append(`<option selected="selected" disabled>Select Center</option>`)
        $('select[name="center"]').selectpicker('refresh');
        for (var i = 0; i < response.data.length; i++) {
          $('select[name="center"]').append(`<option value='${response.data[i].id}'>${response.data[i].center_name}</option>`)
        }
        $('select[name="center"]').selectpicker('refresh');
      }
    });
  }
}
