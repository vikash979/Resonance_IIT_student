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

var page_count = 1;
var max_page = 0;

  $(window).on('load',function(){
      $('#students_page').addClass("active");
      var department_count = 0;
      var conditions = {};
      var paginations = {};
      paginations.page = 1;
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
                          department_count+=1;
                      }
                  }
              }
          });
  });

      // $(' aside .aside-container li.active').addClass('open').children('ul').show();
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


      // let tableData = [
      //     { id: '1', name: 'matish', class: 'class name1' , program: 'program1', phase: 'phase1', currentbatch: 'current batch1', session: '20xx-xx1', center: 'center1' , division: 'division1'},
      //     { id: '2', name: 'satish' , class: 'class name2' , program: 'program2', phase: 'phase2', currentbatch: 'current batch2', session: '20xx-xx2' , center: 'center2' , division: 'division2'},
      //     { id: '3', name: 'mohit' , class: 'class name3' , program: 'program3', phase: 'phase3', currentbatch: 'current batch3', session: '20xx-xx3',center: 'center3' , division: 'division3'},
      //     { id: '4', name: 'abhishek' , class: 'class name4' , program: 'program4', phase: 'phase4', currentbatch: 'current batch4', session: '20xx-xx4', center: 'center4' , division: 'division4'},
      //     { id: '5', name: 'sachin' , class: 'class name5' , program: 'program5', phase: 'phase5', currentbatch: 'current batch5', session: '20xx-xx5', center: 'center5' , division: 'division5'}
          
      // ]


      // let paginationData = [
      //    { id: '1', name: 'matish', class: 'class name1' , program: 'program1', phase: 'phase1', currentbatch: 'current batch1', session: '20xx-xx1', center: 'center1' , division: 'division1'},
      //     { id: '2', name: 'satish' , class: 'class name2' , program: 'program2', phase: 'phase2', currentbatch: 'current batch2', session: '20xx-xx2' , center: 'center2' , division: 'division2'},
      //     { id: '3', name: 'mohit' , class: 'class name3' , program: 'program3', phase: 'phase3', currentbatch: 'current batch3', session: '20xx-xx3',center: 'center3' , division: 'division3'},
      //     { id: '4', name: 'abhishek' , class: 'class name4' , program: 'program4', phase: 'phase4', currentbatch: 'current batch4', session: '20xx-xx4', center: 'center4' , division: 'division4'},
      //     { id: '5', name: 'sachin' , class: 'class name5' , program: 'program5', phase: 'phase5', currentbatch: 'current batch5', session: '20xx-xx5', center: 'center5' , division: 'division5'}
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

      jQuery('.add-departments-link ,.add-designation-link, .add-division-link,.add-skills-link').click(function(){
          //jQuery('.filter-section').css('display','flex');
          jQuery('.AddContentDialog').addClass('open');
      });

       jQuery('.AddContentDialog .form-actions a').click(function(){
          jQuery('.AddContentDialog').removeClass('open');
      });


       jQuery('.confirmationDialog .form-actions a').click(function(){
          jQuery('.confirmationDialog').removeClass('open');
      });

     

  
  

  //     let programFilterData = [];
  //     let phaseFilterData = [];
  //     let currentbatchFilterData = [];
  //     let sessionFilterData = [];
  //     let centersFilterData = [];
  //     let divisionFilterData = [];
      
  //     let tableHTML ='';
  //     let paginationHTML ='';


  //     tableData.forEach((val)=>{
  //         programFilterData.push(val.program);
  //         phaseFilterData.push(val.phase);
  //         currentbatchFilterData.push(val.currentbatch);
  //         sessionFilterData.push(val.session);
  //         centersFilterData.push(val.center);
  //         divisionFilterData.push(val.division);
  //         tableHTML += `<tr>
  //                     <td>
  //                         <div class="usersProfile">
  //                             <div class="thumb"></div>
  //                             <div class="thumb-content">
  //                                 <a href="#">${val.name}</a>
  //                                 <div><span>${val.class}</span></div>
  //                             </div>
  //                         </div>
  //                     </td>
  //                     <td>${val.program}</td>
  //                     <td>${val.phase}</td>
  //                     <td>${val.currentbatch}</td>
  //                     <td>${val.session}</td>
  //                     <td><a href="#"><i class="fa fa-pencil"></i></a><a href="#"><i class="fa fa-trash"></i></a><a href="#"><i class="fa fa-cog"></i></a></td>
  //                 </tr>`;

                  
  //     });

      

  //    let programFilterHTML = '';
  //     programFilterData.forEach((val)=>{
  //         programFilterHTML += `<li><label><input type="checkbox" value="${val}" class="programcheckbox">${val}</label></li>`;
  //     });

  //     let phaseFilterHTML = '';
  //     phaseFilterData.forEach((val)=>{
  //         phaseFilterHTML += `<li><label><input type="checkbox" value="${val}" class="phasecheckbox">${val}</label></li>`;
  //     });

  //     let currentbatchFilterHTML = '';
  //     currentbatchFilterData.forEach((val)=>{
  //         currentbatchFilterHTML += `<li><label><input type="checkbox" value="${val}" class="currentbatchcheckbox">${val}</label></li>`;
  //     });

  //     let sessionFilterHTML = '';
  //     sessionFilterData.forEach((val)=>{
  //         sessionFilterHTML += `<li><label><input type="checkbox" value="${val}" class="sessioncheckbox">${val}</label></li>`;
  //     });

  //     let centersFilterHTML = '';
  //    centersFilterData.forEach((val)=>{
  //         centersFilterHTML += `<li><label><input type="checkbox" value="${val}" class="centerscheckbox">${val}</label></li>`;
  //     });

  //     let divisionFilterHTML = '';
  //    divisionFilterData.forEach((val)=>{
  //         divisionFilterHTML += `<li><label><input type="checkbox" value="${val}" class="divisioncheckbox">${val}</label></li>`;
  //     });

   

  //     jQuery('.listingtable').append(tableHTML);
  //     jQuery('.programFilter').append(programFilterHTML);
  //     jQuery('.phaseFilter').append(phaseFilterHTML);
  //     jQuery('.currentbatchFilter').append(currentbatchFilterHTML);
  //     jQuery('.sessionFilter').append(sessionFilterHTML);
  //     jQuery('.centersFilter').append(centersFilterHTML);
  //     jQuery('.divisionFilter').append(divisionFilterHTML);
     



      jQuery('#txt-search').keyup(function(e){
          let searchValue = $(this).val().toLowerCase();
               console.log(searchValue);
               console.log(tableData);
               let getData = tableData.find(data => data.name === searchValue);
               console.log(getData);
     
          });


      // jQuery('.filterApplyBtn').click(function(){

      //         let filterApplyData = {};
      //         let programFilterdata = [];
      //         let phaseFilterData = [];
      //         let currentbatchFilterData = [];
      //         let sessionsfilterData = [];
      //         let centersFilterData = [];
      //         let divisionFilterData = [];
             


      //         jQuery.each(jQuery(".programcheckbox:checked"), function(){
      //            programFilterdata.push($(this).val());
      //         });

      //         jQuery.each(jQuery(".phasecheckbox:checked"), function(){
      //             phaseFilterData.push($(this).val());
      //         });

      //         jQuery.each(jQuery(".currentbatchcheckbox:checked"), function(){
      //             currentbatchFilterData.push($(this).val());
      //         });

      //         jQuery.each(jQuery(".sessioncheckbox:checked"), function(){
      //             sessionsfilterData.push($(this).val());
      //         });

      //         jQuery.each(jQuery(".centerscheckbox:checked"), function(){
      //            centersFilterData.push($(this).val());
      //         });

      //         jQuery.each(jQuery(".divisioncheckbox:checked"), function(){
      //             divisionFilterData.push($(this).val());
      //         });

             
             


      //         let typeprogram = JSON.stringify(programFilterdata);
      //         let typephase = JSON.stringify(phaseFilterData);
      //         let typecurrentbatch = JSON.stringify(currentbatchFilterData);
      //         let typesession = JSON.stringify(sessionsfilterData);
      //         let typecenters = JSON.stringify(centersFilterData);
      //         let typedivision = JSON.stringify(divisionFilterData);
              
      //         filterApplyData.program=typeprogram;
      //         filterApplyData.phase=typephase;
      //         filterApplyData.currentbatch=typecurrentbatch;
      //         filterApplyData.session=typesession;
      //         filterApplyData.centers=typecenters;
      //         filterApplyData.division=typedivision;
              
              // console.log("filteredApplyData" + filterApplyData.program);
              // console.log("filteredApplyData" + filterApplyData.phase);
              // console.log("filteredApplyData" + filterApplyData.currentbatch);
              // console.log("filteredApplyData" + filterApplyData.session);
              // console.log("filteredApplyData" + filterApplyData.centers);
              // console.log("filteredApplyData" + filterApplyData.division);
              
          // });
  });

$(document).ready(function(){
  $.ajax({
  url: BASE_SITE_URL + `/api/v1/auth/country/`,
  type: 'GET',
  success: function(response){
    var country_input = $('select[name="country"]');
    for (var i=0;i<response.data.length;i++) {
      country_input.append(`<option value='${response.data[i].id}'>${response.data[i].country_name}</option>`)
    }
    // $('select[name="country"]').selectpicker('refresh');
  }
});
});

function regionlist(){
if ($('select[name="country"]').val() != "") {
  var country_val = $('select[name="country"]').val();
  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/`,
    type: 'GET',
    async: false,
    success: function(response){
      $('select[name="region"]').empty();
      // $('select[name="region"]').append(`<option selected="selected" disabled>Select Region</option>`)
      // $('select[name="region"]').selectpicker('refresh');
      for (var i = 0; i < response.data.length; i++) {
          $('select[name="region"]').append(`<option value='${response.data[i].id}'>${response.data[i].region_name}</option>`)

      }
      // $('select[name="region"]').selectpicker('refresh');
    }
  });
}
}

function statelist(){
if ($('select[name="region"]').val() != ""){
  var country_val = $('select[name="country"]').val();
  var region_val = $('select[name="region"]').val();
  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/${region_val}/`,
    type: 'GET',
    async: false,
    success: function(response){
      $('select[name="state"]').empty();
      $('select[name="state"]').append(`<option selected="selected" disabled>Select State</option>`)
      // $('select[name="state"]').selectpicker('refresh');
      for (var i = 0; i < response.data.length; i++) {
        $('select[name="state"]').append(`<option value='${response.data[i].id}'>${response.data[i].state_name}</option>`)
      }
      // $('select[name="state"]').selectpicker('refresh');
    }
  });
}
}

function citylist(){
if ($('select[name="state"]').val() != ""){
  var country_val = $('select[name="country"]').val();
  var region_val = $('select[name="region"]').val();
  var state_val = $('select[name="state"]').val();
  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/${region_val}/${state_val}/`,
    type: 'GET',
    async: false,
    success: function(response){
      $('select[name="city"]').empty();
      $('select[name="city"]').append(`<option selected="selected" disabled>Select City</option>`)
      // $('select[name="city"]').selectpicker('refresh');
      for (var i = 0; i < response.data.length; i++) {
        $('select[name="city"]').append(`<option value='${response.data[i].id}'>${response.data[i].city_name}</option>`)
      }
      // $('select[name="city"]').selectpicker('refresh');
    }
  })
}
}

function centerlist(){
if ($('select[name="city"]').val() != ""){
  var country_val = $('select[name="country"]').val();
  var region_val = $('select[name="region"]').val();
  var state_val = $('select[name="state"]').val();
  var city_val = $('select[name="city"]').val();
  $.ajax({
    url: BASE_SITE_URL + `/api/v1/auth/country/${country_val}/${region_val}/${state_val}/${city_val}/`,
    type: 'GET',
    async: false,
    success: function(response){
      $('select[name="center"]').empty();
      $('select[name="center"]').append(`<option selected="selected" disabled>Select Center</option>`)
      // $('select[name="center"]').selectpicker('refresh');
      for (var i = 0; i < response.data.length; i++) {
        $('select[name="center"]').append(`<option value='${response.data[i].id}'>${response.data[i].center_name}</option>`)
      }
      // $('select[name="center"]').selectpicker('refresh');
    }
  });
}
}

$("#student_form").on('submit', function(e){
  e.preventDefault();
  var req_data = new Object;
  req_data.action = 'create';
  req_data.data = JSON.stringify($(this).serializeObject());
  // console.log(req_data);
  $.ajax({
      url: BASE_SITE_URL + `/api/v1/auth/student/`,
      type: 'POST',
      data: req_data,
      success: function(response){
          console.log(response);
      }
  });
});