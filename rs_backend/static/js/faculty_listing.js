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

var page_count = 1;
var max_page = 0;

var faculty_page_count = 1;
var faculty_max_page = 0;

  $(window).on('load',function(){
        $('#faculties_page').addClass("active");
        faculty_count = 0;
        var conditions = {};
        var paginations = {};
        paginations.page = 1;
        var data = {};
        data.action="view";   
        data.conditions=JSON.stringify(conditions);
        data.paginations = JSON.stringify(paginations);
        $.ajax({
          url: BASE_SITE_URL + `/api/v1/auth/faculty/`,
          type: "POST",
          dataType: "json",
          data:{"action":"view", 'pagination': `${faculty_page_count}`},
          success: function(response){
              for(var i=0;i<response.data.length;i++){
                  $('.listingtable').append(`<tr>
                  <td>
                      <div class="usersProfile">
                          <div class="thumb"></div>
                          <div class="thumb-content">
                              <a href="#">${response.data[i].name}</a>
                                      <div><span>${response.data[i].department.department}</span></div>
                                      <div><span>${response.data[i].designation.designation}</span></div>
                                      <div><span>${response.data[i].user.roles}</span></div>
                              </div>
                      </div>
                  </td>
                                  
                  <td>${response.data[i].center.center_name}</td>
                  <td>${response.data[i].subjects.id}</td>
                  <td><a href="javascript:void(0);" onclick="stor_update_id(${response.data[i].id});"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="delete_faculty(${response.data[i].id});"><i class="fa fa-trash"></i></a><a href="javascript:void(0);"><i class="fa fa-cog"></i></a></td>
                  </tr>`);

                  faculty_count+=1;
                  faculty_max_page = response.data[i].num_pages;
                } 
                $('#faculty_count').html(faculty_count);
                $('.paginationContainer').append(`<a href="javascript:void(0);">prev</a>`)
                for(var i=0; i < faculty_max_page; i++){
                    var value = i
                    if (value == 0){
                        $('.paginationContainer').append(`<a href="javascript:void(0);" class="selected">${++value}</a>`)
                    } else {
                        $('.paginationContainer').append(`<a href="javascript:void(0);">${++value}</a>`)
                    }
                }
                $('.paginationContainer').append(`<a href="javascript:void(0);">next</a>`)
                set_fculty_pginator()
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
                  $('.designationFilter').append(`<li><label><input type="checkbox" value="${response.data[i].designation}" class="designationcheckbox">${response.data[i].designation}</label></li>`);
                }  
          }
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
                $('.ETFilter').append(`<li><label><input type="checkbox" value="${response.data[i].et_name}" class="etcheckbox">${response.data[i].et_name}</label></li>`);
              }  
        }
    }
    });

function set_fculty_pginator(){
        $('.paginationContainer a').on('click', function(e){
            $('.paginationContainer a').removeClass('selected');
            var currBtn = e.target;
            $(currBtn).addClass('selected');
            if($(currBtn).html()=="prev"){
                if(faculty_page_count==1){
                    faculty_page_count = 1;
                }
                else{
                    faculty_page_count-=1;
                }
            }
            else if($(currBtn).html()=="next"){
                if(faculty_page_count == faculty_max_page){
                    faculty_page_count=faculty_max_page;
                }
                else{
                    faculty_page_count+=1;
                }
                
            }
            else{
                faculty_page_count = $(currBtn).html();
            }
            $('.listingtable').empty();
        $.ajax({
          url: BASE_SITE_URL + `/api/v1/auth/faculty/`,
          type: "POST",
          dataType: "json",
          data:{"action":"view", 'pagination': `${faculty_page_count}`},
          success: function(response){
              for(var i=0;i<response.data.length;i++){
                  $('.listingtable').append(`<tr>
                  <td>
                      <div class="usersProfile">
                          <div class="thumb"></div>
                          <div class="thumb-content">
                              <a href="#">${response.data[i].name}</a>
                                      <div><span>${response.data[i].department.department}</span></div>
                                      <div><span>${response.data[i].designation.designation}</span></div>
                                      <div><span>${response.data[i].user.roles}</span></div>
                              </div>
                      </div>
                  </td>
                                  
                  <td>${response.data[i].center.center_name}</td>
                  <td>${response.data[i].subjects.id}</td>
                  <td><a href="javascript:void(0);" onclick="stor_update_id(${response.data[i].id});"><i class="fa fa-pencil"></i></a><a href="javascript:void(0);" onclick="delete_faculty(${response.data[i].id});"><i class="fa fa-trash"></i></a><a href="javascript:void(0);"><i class="fa fa-cog"></i></a></td>
                  </tr>`);

                  faculty_count+=1;
                } 
          }
      });
  })
}

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
                    $('.departmentFilter').append(`<li><label><input type="checkbox" value="${response.data[i].department}" class="departmentcheckbox">${response.data[i].department}</label></li>`);
                  }
              }
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
        url: BASE_SITE_URL + `/api/v1/subject/master_subject/`,
        type: "POST",
        dataType: "json",
        data:data,
        success: function(response){
            if (response.status != false) {
                for(var i=0;i<response.data.length;i++){
                    $('.subjectsFilter').append(`<li><label><input type="checkbox" value="${response.data[i].name}" class="subjectscheckbox">${response.data[i].name}</label></li>`);
                  }
              }
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
        url: BASE_SITE_URL + `/api/v1/auth/division/`,
        type: "POST",
        dataType: "json",
        data:data,
        success: function(response){
            if (response.status != false) {
                for(var i=0;i<response.data.length;i++){
                    $('.divisionFilter').append(`<li><label><input type="checkbox" value="${response.data[i].division}" class="divisioncheckbox">${response.data[i].division}</label></li>`);
                  }
              }
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
            $('.skillFilter').append(`<li><label><input type="checkbox" value="${response.data[i].id}" class="divisioncheckbox">${response.data[i].skill}</label></li>`);
        }
        }
  }
});

    $.ajax({
        url: BASE_SITE_URL + `/api/v1/institute/batches/`,
        type: "POST",
        dataType: "json",
        data:{"action":"view"},
        success: function(response){
            if (response.status != false) {
                for(var i=0;i<response.data.length;i++){
                    $('.batchFilter').append(`<li><label><input type="checkbox" value="${response.data[i].name}" class="batchcheckbox">${response.data[i].name}</label></li>`);
                  }
              }
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

function delete_faculty(attrid){
  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/faculty/`,
    type: 'POST',
    data: {'action': 'remove', 'conditions': JSON.stringify({'id': attrid})},
    success: function(response){
      if(response.status == true){
        window.location.href = '/faculties/';
      }
    }
  });
}


    // let tableData = [
    //     { id: '1', name: 'matish' , roles: 'Roles', division: 'Division', designation: 'designation1', department: 'department2', center: 'Center1', et: 'ET', skills: 'Skills1', batch: 'Batch', subject: 'Subject1'},
    //     { id: '2', name: 'mohit' , roles: 'Roles2', division: 'Division2', designation: 'designation2', department: 'department2', center: 'Center2', et: 'ET2', skills: 'Skills2', batch: 'Batch2', subject: 'Subject2'},
    //     { id: '3', name: 'abhishek' , roles: 'Roles3',  division: 'Division3',designation: 'designation3', department: 'department3', center: 'Center3', et: 'ET3', skills: 'Skills3', batch: 'Batch3', subject: 'Subject3'},
    //     { id: '4', name: 'title4' , roles: 'Roles4', division: 'Division4', designation: 'designation4', department: 'department4', center: 'Center4', et: 'ET4', skills: 'Skills4', batch: 'Batch4', subject: 'Subject4'},
    //     { id: '5', name: 'Title5' , roles: 'Roles5', division: 'Division5', designation: 'designation5', department: 'department5', center: 'Center5', et: 'ET5', skills: 'Skills5', batch: 'Batch5', subject: 'Subject5'}
    // ]


    // let paginationData = [
    //     { id: '1', name: 'matish pagination' , roles: 'Roles', division: 'Division', designation: 'designation1', department: 'department2', center: 'Center1', et: 'ET', skills: 'Skills1', batch: 'Batch', subject: 'Subject1'},
    //     { id: '2', name: 'mohit' , roles: 'Roles2', division: 'Division2', designation: 'designation2', department: 'department2', center: 'Center2', et: 'ET2', skills: 'Skills2', batch: 'Batch2', subject: 'Subject2'},
    //     { id: '3', name: 'abhishek' , roles: 'Roles3',  division: 'Division3',designation: 'designation3', department: 'department3', center: 'Center3', et: 'ET3', skills: 'Skills3', batch: 'Batch3', subject: 'Subject3'},
    //     { id: '4', name: 'title4' , roles: 'Roles4', division: 'Division4', designation: 'designation4', department: 'department4', center: 'Center4', et: 'ET4', skills: 'Skills4', batch: 'Batch4', subject: 'Subject4'},
    //     { id: '5', name: 'Title5' , roles: 'Roles5', division: 'Division5', designation: 'designation5', department: 'department5', center: 'Center5', et: 'ET5', skills: 'Skills5', batch: 'Batch5', subject: 'Subject5'}
    // ]


            function confirmation(type){
                if (type === 'confirm'){
                }else{
                }  
        }

        function success(type){
                if (type === 'ok'){
                }else{
                console.log("cancel"); 
                }  
        }


jQuery(document).ready(function(){

    jQuery('.add-departments-link ,.add-designation-link, .add-division-link, .add-skills-link, .add-et-link, .add-roles-link, .add-centers-link').click(function(){
        jQuery('.AddContentDialog').addClass('open');
    });

        jQuery('.AddContentDialog .form-actions a').click(function(){
        jQuery('.AddContentDialog').removeClass('open');
    });


        jQuery('.confirmationDialog .form-actions a').click(function(){
        jQuery('.confirmationDialog').removeClass('open');
    });

    

    // let departmentFilterData = [];
    // let designationFilterData = [];
    // let divisionFilterData = [];
    // let skillsFilterData = [];
    // let etFilterData = [];
    // let rolesFilterData = [];
    // let centersFilterData = [];
    // let subjectsFilterData = [];
    // let batchFilterData = [];
    // let tableHTML ='';
    // let paginationHTML ='';


    // tableData.forEach((val)=>{
    //     departmentFilterData.push(val.department);
    //     designationFilterData.push(val.designation);
    //     divisionFilterData.push(val.division);
    //     skillsFilterData.push(val.skills);
    //     etFilterData.push(val.et);
    //     rolesFilterData.push(val.roles);
    //     centersFilterData.push(val.center);
    //     subjectsFilterData.push(val.subject);
    //     batchFilterData.push(val.batch);
    //     tableHTML += `<tr>
    //                 <td>
    //                     <div class="usersProfile">
    //                         <div class="thumb"></div>
    //                         <div class="thumb-content">
    //                             <a href="#">${val.name}</a>
    //                             <div><span>${val.department}</span></div>
    //                             <div><span>${val.designation}</span></div>
    //                             <div><span>${val.roles}</span></div>
    //                         </div>
    //                     </div>
    //                 </td>
                    
    //                 <td>${val.center}</td>
    //                 <td>${val.subject}</td>
    //                 <td><a href="#"><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a><a href="#"><i class="fa fa-cog"></i></a></td>
    //             </tr>`;

                
    // });

    // jQuery('.paginationWrapper  a').click(function(){
    //     tableHTML ='';
    //     paginationData.forEach((val)=>{
    //     departmentFilterData.push(val.department);
    //     designationFilterData.push(val.designation);
    //     divisionFilterData.push(val.division);
    //     skillsFilterData.push(val.skills);
    //     etFilterData.push(val.et);
    //     rolesFilterData.push(val.roles);
    //     centersFilterData.push(val.center);
    //     subjectsFilterData.push(val.subject);
    //     batchFilterData.push(val.batch);
    //     paginationData += `<tr>
    //                 <td>
    //                     <div class="usersProfile">
    //                         <div class="thumb"></div>
    //                         <div class="thumb-content">
    //                             <a href="#">${val.name}</a>
    //                             <div><span>${val.department}</span></div>
    //                             <div><span>${val.designation}</span></div>
    //                             <div><span>${val.roles}</span></div>
    //                         </div>
    //                     </div>
    //                 </td>
    //                 <td>${val.center}</td>
    //                 <td>${val.subject}</td>
    //                 <td><a href="#"><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a><a href="#"><i class="fa fa-cog"></i></a></td>
    //             </tr>`;

                
    // });
    //     jQuery('.listingtable').append(paginationHTML);

    // });


    // let departmentFilterHTML = '';
    // departmentFilterData.forEach((val)=>{
    //     departmentFilterHTML += `<li><label><input type="checkbox" value="${val}" class="departmentcheckbox">${val}</label></li>`;
    // });

    // let designationFilterHTML = '';
    // designationFilterData.forEach((val)=>{
    //     designationFilterHTML += `<li><label><input type="checkbox" value="${val}" class="designationcheckbox">${val}</label></li>`;
    // });

    // let divisionFilterHTML = '';
    // divisionFilterData.forEach((val)=>{
    //     divisionFilterHTML += `<li><label><input type="checkbox" value="${val}" class="divisioncheckbox">${val}</label></li>`;
    // });

    // let skillsFilterHTML = '';
    // skillsFilterData.forEach((val)=>{
    //     skillsFilterHTML += `<li><label><input type="checkbox" value="${val}" class="skillscheckbox">${val}</label></li>`;
    // });

    // let ETFilterHTML = '';
    // etFilterData.forEach((val)=>{
    //     ETFilterHTML += `<li><label><input type="checkbox" value="${val}" class="etcheckbox">${val}</label></li>`;
    // });

    // let rolesFilterHTML = '';
    // rolesFilterData.forEach((val)=>{
    //     rolesFilterHTML += `<li><label><input type="checkbox" value="${val}" class="rolescheckbox">${val}</label></li>`;
    // });

    // let centersFilterHTML = '';
    // centersFilterData.forEach((val)=>{
    //     centersFilterHTML += `<li><label><input type="checkbox" value="${val}" class="centerscheckbox">${val}</label></li>`;
    // });

    // let subjectsFilterHTML = '';
    // subjectsFilterData.forEach((val)=>{
    //     subjectsFilterHTML += `<li><label><input type="checkbox" value="${val}" class="subjectscheckbox">${val}</label></li>`;
    // });

    // let batchFilterHTML = '';
    // batchFilterData.forEach((val)=>{
    //     batchFilterHTML += `<li><label><input type="checkbox" value="${val}" class="batchcheckbox">${val}</label></li>`;
    // });


    // jQuery('.listingtable').append(tableHTML);
    // jQuery('.departmentFilter').append(departmentFilterHTML);
    // jQuery('.designationFilter').append(designationFilterHTML);
    // jQuery('.divisionFilter').append(divisionFilterHTML);
    // jQuery('.skillsFilter').append(skillsFilterHTML);
    // jQuery('.ETFilter').append(ETFilterHTML);
    // jQuery('.rolesFilter').append(rolesFilterHTML);
    // jQuery('.centersFilter').append(centersFilterHTML);
    // jQuery('.subjectsFilter').append(subjectsFilterHTML);
    // jQuery('.batchFilter').append(batchFilterHTML);



    jQuery('#txt-search').keyup(function(e){
        let searchValue = $(this).val().toLowerCase();
                let getData = tableData.find(data => data.name === searchValue);
    
        });


    jQuery('.filterApplyBtn').click(function(){
            let filterApplyData = {};

            let departmentFilterdata = [];
            let designationFilterData = [];
            let divisionFilterData = [];
            let skillsFilterData = [];
            let etFilterData = [];
            let rolesFilterData = [];
            let centersFilterData = [];
            let subjectsFilterData = [];
            let batchFilterData = [];


            jQuery.each(jQuery(".departmentcheckbox:checked"), function(){
                departmentFilterdata.push($(this).val());
            });

            jQuery.each(jQuery(".designationcheckbox:checked"), function(){
                designationFilterData.push($(this).val());
            });

            jQuery.each(jQuery(".divisioncheckbox:checked"), function(){
                divisionFilterData.push($(this).val());
            });

            jQuery.each(jQuery(".skillscheckbox:checked"), function(){
                skillsFilterData.push($(this).val());
            });

            jQuery.each(jQuery(".etcheckbox:checked"), function(){
                etFilterData.push($(this).val());
            });

            jQuery.each(jQuery(".rolescheckbox:checked"), function(){
                rolesFilterData.push($(this).val());
            });

            jQuery.each(jQuery(".centerscheckbox:checked"), function(){
                centersFilterData.push($(this).val());
            });

            jQuery.each(jQuery(".subjectscheckbox:checked"), function(){
                subjectsFilterData.push($(this).val());
            });

            jQuery.each(jQuery(".batchcheckbox:checked"), function(){
                batchFilterData.push($(this).val());
            });

            


            let typedepartment = JSON.stringify(departmentFilterdata);
            let typedesignation = JSON.stringify(designationFilterData);
            let typedivision = JSON.stringify(divisionFilterData);
            let typeskills = JSON.stringify(skillsFilterData);
            let typeet = JSON.stringify(etFilterData);
            let typeroles = JSON.stringify(rolesFilterData);
            let typecenters = JSON.stringify(centersFilterData);
            let typesubjects = JSON.stringify(subjectsFilterData);
            let typebatch = JSON.stringify(batchFilterData);
            
            filterApplyData.depeartment=typedepartment;
            filterApplyData.designation=typedesignation;
            filterApplyData.division=typedivision;
            filterApplyData.skills=typeskills;
            filterApplyData.et=typeet;
            filterApplyData.roles=typeroles;
            filterApplyData.centers=typecenters;
            filterApplyData.subjects=typesubjects;
            filterApplyData.batch=typebatch;
        });

});

function stor_update_id(attrid){
  localStorage.setItem('faculty_key', attrid);
  window.location.href='/faculties/edit/';
}

$(document).ready(function(){
  if (localStorage.getItem('faculty_key')){
    localStorage.removeItem('faculty_key');
  }
});
