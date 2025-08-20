# scripts/daily_check.py
import os
import json
from datetime import datetime, date
import glob

# 스터디 멤버 리스트 (실제 이름으로 수정하세요!)
MEMBERS = [
    "김강연",  # 실제 이름으로 변경
    "홍길동",  # 실제 이름으로 변경  
    "김철수",  # 실제 이름으로 변경
    "이영희",  # 실제 이름으로 변경
    "박민수"   # 실제 이름으로 변경
]

def get_current_week_folder():
    """현재 주차 폴더명 반환"""
    # 8월 3주차, 8월 4주차 등의 형태로 가정
    today = date.today()
    month = today.month
    
    # 간단한 주차 계산 (실제 상황에 맞게 수정 필요)
    if today.day <= 7:
        week = 1
    elif today.day <= 14:
        week = 2
    elif today.day <= 21:
        week = 3
    else:
        week = 4
    
    return f"{month}월{week}주차"

def get_today_folder():
    """오늘 날짜 폴더명 반환 (MMDD 형식)"""
    return datetime.now().strftime("%m%d")

def check_today_uploads():
    """오늘 업로드된 파일들 체크"""
    week_folder = get_current_week_folder()
    today_folder = get_today_folder()
    
    folder_path = f"{week_folder}/{today_folder}"
    
    print(f"🔍 체크 경로: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"❌ 오늘 폴더가 존재하지 않습니다: {folder_path}")
        return {}
    
    # 각 멤버별 업로드 현황 체크
    upload_status = {}
    
    for member in MEMBERS:
        member_files = []
        
        # 해당 폴더에서 멤버 이름이 포함된 파일 찾기
        for file in os.listdir(folder_path):
            if member in file and file.endswith('.py'):
                member_files.append(file)
        
        upload_status[member] = {
            'uploaded_count': len(member_files),
            'files': member_files,
            'status': '✅' if len(member_files) > 0 else '❌'
        }
    
    return upload_status

def print_daily_report(upload_status):
    """일일 리포트 출력"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n📊 알고리즘 스터디 일일 리포트 ({today})")
    print("=" * 50)
    
    total_uploaded = 0
    total_members = len(MEMBERS)
    
    for member, status in upload_status.items():
        status_icon = status['status']
        file_count = status['uploaded_count']
        
        print(f"{status_icon} {member}: {file_count}개 문제 업로드")
        
        if file_count > 0:
            total_uploaded += 1
            for file in status['files']:
                print(f"   📝 {file}")
    
    print(f"\n📈 전체 현황: {total_uploaded}/{total_members}명 참여 ({(total_uploaded/total_members)*100:.1f}%)")
    
    # 아직 업로드하지 않은 멤버들
    not_uploaded = [member for member, status in upload_status.items() if status['uploaded_count'] == 0]
    
    if not_uploaded:
        print(f"\n🔔 아직 업로드하지 않은 멤버:")
        for member in not_uploaded:
            print(f"   ⏰ {member}")
    else:
        print(f"\n🎉 모든 멤버가 오늘 문제를 업로드했습니다!")

def save_daily_log(upload_status):
    """일일 로그를 JSON 파일로 저장"""
    today = datetime.now().strftime("%Y%m%d")
    log_dir = "logs"
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_data = {
        'date': today,
        'upload_status': upload_status,
        'timestamp': datetime.now().isoformat()
    }
    
    log_file = f"{log_dir}/daily_log_{today}.json"
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 일일 로그 저장: {log_file}")

if __name__ == "__main__":
    print("🚀 일일 알고리즘 스터디 체크 시작!")
    
    try:
        upload_status = check_today_uploads()
        print_daily_report(upload_status)
        save_daily_log(upload_status)
        
        print("\n✅ 일일 체크 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()