$(window).on('load',function(){
    $('#programspage').addClass("active");
    $(' aside .aside-container li.active').addClass('open').children('ul').show();
    $('#phase_page').addClass("active");
  //lert(JSON.stringify({"action":"view","identr":"identr"}))

    $.ajax({
          url: BASE_SITE_URL + '/api/v1/institute/session_has_program/',
          type: "POST",
          dataType: "json",
          data:{"action":"view","identr":"identr"},
          success: function(response){
              $('#programdds').append(`<option value=---" >----Select Program(Session)---</option>`);
              for (var i=0;i<response.data.length;i++)
              {
                  console.log("ssss"+response.data[i].id)
                  //alert(JSON.stringify(response.data[i].program.display_name))
                 // $('select[name="programss"] option:selected').val(response.data[i].name);
                  
                      //alert(response.data[i].name)
                 // $('#phasesdd').append(`<option value="${response.data[i].id}" selected="selected">${response.data[i].name}</option>`);
                  $('#programdds').append(`<option value="${response.data[i].id}" >${response.data[i].program.display_name}(${response.data[i].session['display_name']})</option>`);
                      
                  
              }
           
  
          }
      })
  
  
     
   
      classpagination()
  })
  
  
  
  function classpagination(class_count)
  {
      if (class_count== undefined)
      {
          $.ajax({
              url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
              type: "POST",
              dataType: "json",
              data:{"action":"view"},
              success: function(response){
                  if (response.status==true)
                  {
                      let lineNo = 1;
                      tableBody = $("table tbody");
                      let tableData = JSON.stringify(response.data)
                      $('#listingtable').html('')
                      $('#pagination').html('')
                      for(var i=0;i<response.data.length;i++){
                          //alert(response.data[i].id,response.data[i].program_session)
  
                          session_obj(response.data[i].id,response.data[i].program_session)
                   
                      var totalrecord = (response.data[i].id+"_"+response.data[i].display_name+"_"+response.data[i].order+"_"+response.data[i].name+"_"+response.data[i].description)
                     
                      //$('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].order}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td><a href="class-subjects-details.html" class=' create-subjects-link'><i class="fa fa-plus"></i>Create  Subjects</a></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                      $('#listingtable').append(`<tr> <td>    ${response.data[i].name}</td><td>${response.data[i].display_name}</td><td>${response.data[i].description}</td><td>${response.data[i].start_date}</td><td>${response.data[i].end_date}</td><td><span class=' create-subjects-link' id="${response.data[i].id}"></span></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i><a href='javascript:void(0);' onclick="editClassBatch(${response.data[i].id})" class='edit-link'>Batches</i></a></td></tr>`)
                      }
                      var pagi_length =response.paginations['class_numpage']+1
                       
                      if (response.paginations['class_numpage'] > 0){
                          if(response.paginations['class_user_changes']==true)
                          {
                             if(response.paginations['class_previous']==true){
     
                                 $('#pagination').append(`<a href="#">prev</a>`)
                                 
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
                                  
                                 $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="classpagination(${i});">${i}</a>`)
                              }
                             }
                             if (response.paginations['class_next']==true)
                             {
                                 $('#pagination').append(`<a href="#" onclick="classpagination(${response.paginations['class_next_page_number']});">next</a>`)
                             }
                             
                          }
                          //location.reload();
                      }
                  }
                  
              }
          })
      }
      else{
  
          $.ajax({
              url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
              type: "POST",
              dataType: "json",
              data:{"action":"view","page":class_count},
              success: function(response){
                  if (response.status==true)
                  {
                      $('#listingtable').html('')
                       $('#pagination').html(' ')
                      for(var i=0;i<response.data.length;i++){
                          session_obj(response.data[i].id,response.data[i].program_session)
                      
                      var totalrecord = (response.data[i].id+"_"+response.data[i].name+"_"+response.data[i].display_name+"_"+response.data[i].description+"_"+response.data[i].start_date)
                      //alert(totalrecord)
                      $('#listingtable').append(`<tr> <td>    ${response.data[i].name}</td><td>${response.data[i].display_name}</td><td>${response.data[i].description}</td><td>${response.data[i].start_date}</td><td>${response.data[i].end_date}</td><td><a href="#"  id="${response.data[i].id}"class=' create-subjects-link'></a></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
                    
                      }
                      var pagi_length =response.paginations['class_numpage']+1
                       
                      if (response.paginations['class_numpage'] > 0){
                          
                          if(response.paginations['class_user_changes']==true)
                          {
                             if(response.paginations['class_previous']==true){
     
                                 $('#pagination').append(`<a href="#" onclick="classpagination(${response.paginations['class_previous_page']})">prev</a>`)
                                 
                             }
                             // else{
                             //     $('#pagination').append(`<span>prev</span>`)
                             // }
                             for (var i=1;i<pagi_length;i++)
                             {
                              if (response.paginations['current_page']==i)
                              {
                                  
                                 $('#pagination').append(`<a href="#" onclick="classpagination(${i}") class="selected">${i}</a>`)
                              }  
                              else{
                                  
                                 $('#pagination').append(`<a href="#" class="paginate" id="${i}" onclick="classpagination(${i});">${i}</a>`)
                              }
                             }
                             if (response.paginations['class_next']==true)
                             {
                                 $('#pagination').append(`<a href="#" onclick="classpagination(${response.paginations['class_next_page_number']})">next</a>`)
                             }
                             
                          }
                          //location.reload();
                      }
                  }
                  
              }
          })
      }
    
  
  }
  
  ////////////////////View Id/////////////////////////////
  function session_rec(session_id,attrId)
  {
      //alert(session_id)
      $.ajax({
          url: BASE_SITE_URL + '/api/v1/institute/sessions/',
          type: "POST",
          dataType: "json",
          data:{"action":"view","id":session_id},
          success: function(response){
             //alert(JSON.stringify(response.data))
  
          }
      })
      
  }
  
  function  editClassBatch(attrId)
  {
    $('#edit_batches').click( function(e){
        $('#hidden_batch_id').val(attrId)

    var name = $('#title_batch').val()
    var start_date = $('#startdatepicker_batch').val()
    var end_date = $('#enddatepicker_batch').val()
   var display_name =  $('#uniquecode_batch').val()
    var description = $('#description_batch').val()
    var times_slot = $('#time_batch').val()
    var phase =attrId
    dataString = {"action":"add","times_slot":times_slot,"display_name":display_name,"description":description,"name":name,"phase":phase,"start_date":start_date,"end_date":end_date}
    $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/batches/',
        type: "POST",
        dataType: "json",
        data:dataString,
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

    })
    
    $('#add_batch').addClass('open');
    console.log("after")
    // jQuery('.addSessionDialogbatch').addClass('open');
  }
  
  //////////////////////////////////////////////////////
  
  function editClass(attrId)
  {
      //dataString = {"action":"view","conditions":{"page":attrId}}
      //alert(JSON.stringify(dataString))
  
      $.ajax({
        url: BASE_SITE_URL + '/api/v1/institute/session_has_program/',
        type: "POST",
        dataType: "json",
        data:{"action":"view","identr":"identr"},
          success: function(response){
              var i = 0
              $('#phasesdd').append(`<option value=---" >----Select Program(Session)---</option>`);
              for (var i=0;i<response.data.length;i++)
              {
                  
                //alert(response.data)
                 //console.log(response.data[i].id)
                 //alert(response.data[i])
                 //$('#phasesdd').append(`<option value="${response.data[i].id}">${response.data[i].name}</option>`);
                 
                  $('#phasesdd').append(`<option value="${response.data[i].id}" >${response.data[i].program.display_name}(${response.data[i].session['display_name']})</option>`);
                
                  
              }
              //$('#phasesdd').selectpicker('refresh');
  
          }
      })
      var hidden_class_id = $('#hidden_class_id').val(attrId)
      var  cl_id = $('#hidden_class_id').val()
      var conditions = {};
          conditions.id = attrId;
          var data = {};
          data.action="view";   
          data.conditions=JSON.stringify(conditions);
  
          $.ajax({
              url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
              type: "POST",
              dataType: "json",
              data:{"action":"view","id":attrId},
              success: function(response){
                  
                  if (response.status ==true){
                     // alert(JSON.stringify(response.data))
                      
                      var class_saved = "Success Fully Saved"
                      var title = $('#title').val(response.data[0]['name'])
                      var description = $('#description').val(response.data[0]['description'])
                      var name = $('#uniquecode').val(response.data[0]['display_name'])
                      var start_date = response.data[0]['start_date']
                      var startdate = start_date.split("-")
                      var month = startdate[1]
                      var dates = startdate[2]
                      var year = startdate[0]
                      var startdate = month + "/"+dates+"/"+year
                      $('#startdatepicker').val(startdate)
                      session_id = response.data[0]['program_session']
                      //alert(session_id)

                      var end_date = response.data[0]['end_date']
                      var enddate = end_date.split("-")
                      var end_month = enddate[1]
                      var end_dates = enddate[2]
                      var end_year = enddate[0]
                      var end_date = end_month + "/"+end_dates+"/"+end_year
                      $('#enddatepicker').val(end_date)
                      //session_obj(session_id)
                      var name = $('#shortcode').val(startdate)
                      // var order = $('#order').val(response.data[0]['order'])
                      // dataString  = {"name":name,"display_name":display_name,"description":description,"order":order}
                      // var addclass = $('#addclass').hide()
                      // var update = $('#update').show()
                     
                  }
                  else{
                      var class_saved = "Failed"
                  }
                 
              }
          })
          jQuery('.addSessionDialog.foredit').addClass('open');
         
  
  }
  
  
  ////////////////////////////////////////////////////////////////////////////
  
  
  
  function updateclass()
  {
      var display_name = $('#title').val()
      var description = $('#description').val()
      var name = $('#uniquecode').val()
      var  cl_id = $('#hidden_class_id').val()
      var start_date = $('#startdatepicker').val()
      var start_dt = start_date.split("/")
      var session = $('#phasesdd').val()
      star_month = start_dt[0]
      star_date = start_dt[1]
      star_year = start_dt[2]
      start_date = star_year+"-"+star_month+"-"+star_date
      var end_date = $('#enddatepicker').val()
      var end_dt = end_date.split("/")
      end_month = start_dt[0]
      end_date = start_dt[1]
      end_year = start_dt[2]
      end_date = end_year+"-"+end_month+"-"+end_date
      dataString  = {"action":"Update","name":name,"display_name":display_name,"description":description,"id": cl_id,"start_date":start_date,"end_date":end_date,"session":session}
      //alert(JSON.stringify(dataString))
      $.ajax({
          url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
          type: "POST",
          dataType: "json",
          data:dataString,
          success: function(response){
              //alert(JSON.stringify(response.data))
             
              var display_name = $('#title').val(' ')
              var description = $('#description').val(' ')
              var name = $('#shortcode').val(' ')
              var order = $('#order').val(' ')
              location.reload();
  
          }
      })
  }
  
  
  
  
  ////////////////////////remove////////////////////////////////////////////////////
  
  function remove(removeid)
  {
      $.ajax({
          url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
          type: "POST",
          dataType: "json",
          data:{"action":"remove","id":removeid},
          success: function(response){
              //alert(JSON.stringify(response.status))
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
  
  
  $("#add_submit").click( function(e){
      var display_name = $('#phase_title').val()
      var description = $('#phase_description').val()
      var name = $('#phase_uniquecode').val()
      
      var start_date = $('#phase_start').val()
      var start_dt = start_date.split("/")
      var session = $('#programdds').val()
      star_month = start_dt[0]
      star_date = start_dt[1]
      star_year = start_dt[2]
      start_date = star_year+"-"+star_month+"-"+star_date
      var end_date = $('#phase_end').val()
      var end_dt = end_date.split("/")
      end_month = start_dt[0]
      end_date = start_dt[1]
      end_year = start_dt[2]
      end_date = end_year+"-"+end_month+"-"+end_date
      dataString  = {"action":"add","name":name,"display_name":display_name,"description":description,"start_date":start_date,"end_date":end_date,"session":session}
      //alert(JSON.stringify(dataString))
      $.ajax({
          url: BASE_SITE_URL + '/api/v1/institute/phasehassession/',
          type: "POST",
          dataType: "json",
          data:dataString,
          success: function(response){
              //alert(JSON.stringify(response.status))
              if (response.status ==true){
                  var class_saved = "Success Fully Saved"
                  
                  location.reload();
  
              }
              else{
                  var class_saved = "Failed"
              }
              
          }
  
     })
  
  })
  
  
  
  function session_obj(tdId,sessionId)
  {
      $.ajax({
          url: BASE_SITE_URL + '/api/v1/institute/session_has_program/',
          type: "POST",
          dataType: "json",
          data:{"action":"view","id":sessionId},
          success: function(response){
              for (var i=0;i<response.data.length;i++)
              {
                  //alert(JSON.stringify(response.data[i]))
                  $('#'+tdId).html(response.data[i].program.name+"-"+"("+response.data[i].session.name+")")
                 // $('select[name="programss"] option:selected').val(response.data[i].name);
                  
                      //alert(response.data[i].name)
                   //$('#add_phase').append(`<option value="${response.data[i].id}" selected="selected">${response.data[i].name}</option>`);
                      
                  
              }
           
  
          }
      })
  }

  function openPopup(){
      $('#openPopUp').addClass('open');
  }
  
  
  
  //////////////////////////////////////////////
  
  // function session_obj(sessionId)
  // {
  //     $.ajax({
  //         url: BASE_SITE_URL + '/api/v1/institute/sessions/',
  //         type: "POST",
  //         dataType: "json",
  //         data:{"action":"view"},
  //         success: function(response){
  //             $('#total_session').text(response.data.length)
  //             //alert(JSON.stringify(response.data))
              
  //             if (response.data.length > 0)
  //             {
  //                 for(var i=0;i<response.data.length;i++){
  //                    // alert(response.data)
  //                // $('#listingtable').append(`<tr> <td>    ${response.data[i].display_name}</td><td>${response.data[i].name}</td><td>${response.data[i].description}</td><td></td><td><a href='javascript:void(0);' onclick="editClass(${response.data[i].id})" class='edit-link'><i class='fa fa-pencil'></i></a><a href="#" onclick="remove(${response.data[i].id})"><i class="fa fa-trash"></i></a></td></tr>`)
  //                 }
  
  //             }
  //             else{
  //                 //$('#listingtable').append(`<tr> <td colspan="4">There is no record</td></tr>`)
  //             }
  
              
                   
             
  //         }
  //     })
  // }