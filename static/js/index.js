
function popup_open(id) {
	id.classList.add("show");
}
function popup_close(id) {
	id.classList.remove("show");
}

function job_check(content,array,id){
	if (content.checked == true){
		for(i=0; i<array.length; i++){
			const temp = document.createElement("div")
			temp.innerHTML = '<div class="cb"><input type="checkbox" id='+id[i]+' name="job_detail" onClick = "checkSmallOnlyOne(this)"><label for='+id[i]+'><span class="cbText">'+array[i]+'</span></label></div>'
			document.getElementById("job_result").append(temp);
		}
	}
	else{
		document.getElementById("job_result").innerText = "";
	}
}

function checkOnlyOne(element) {
  
	const checkboxes = document.getElementsByName("job_main");
	
	checkboxes.forEach((cb) => {
	  cb.checked = false;
	})
	document.getElementById("job_result").innerText = "";
	element.checked = true;
}

function checkSmallOnlyOne(element) {
  
	const checkboxes = document.getElementsByName("job_detail");
	
	checkboxes.forEach((cb) => {
	  cb.checked = false;
	})
	element.checked = true;
}

function questionDefaultCheck(value) {
	if (value == "other") {
		document.getElementById("question_list").remove();
		document.querySelector(".question").innerHTML = '<textarea list="question_list" name="" id="" placeholder="자소서 문항을 입력하세요.(지원동기, 포부 등)" rows="1" cols="30" maxlength="30"></textarea>'
	}
}


function listShow(){
	const no_data = document.getElementById("no-data");
	no_data.classList.add("hide");
	const exist_data = document.getElementById("exist-data");
	exist_data.classList.add("show");
}


// RecommendLog
// fetch(
//   # 백엔드 서버로 유저 로그 전송
// ).then(
//   success면 그냥 오케이
// ).catch(
//   어쩌라고?? 에러 ㅇㅋㅇㅋ 서버가 응답하지 않습니다
// )

// fetch(
// 	# 백엔드 서버로 유저 정보 전송해서 리스폰스 확인
// ).then(
//   exist_data에 파싱해서 넣는 함수 호출
// ).catch(

// )

// => 이걸 하려면 백엔드에서 어떤 형식으로 데이터를 받아올지 명확하게 정의해야 함.
//  - [[], [], [], [], []] 리스트 원소가 다섯 개인 이차원 리스트로 받기!
 

// AnswerLog
// 개별 자소서를 클릭할 떄마다 로그를 남긴다