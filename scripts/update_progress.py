# scripts/update_progress.py - 문제별 폴더 구조 완전 대응 버전
import os
import re
import json
from datetime import datetime, date
from collections import defaultdict

# 스터디 멤버 리스트 (실제 이름으로 업데이트)
MEMBERS = [
    "김강연",
    "신재혁", 
    "오창민",
    "송민경",
    "최재각" 
]

def find_all_week_folders():
    """모든 주차 폴더 찾기"""
    week_folders = []
    
    try:
        items = os.listdir('.')
        print(f"📂 루트 디렉토리 내용: {items}")
        
        for item in items:
            if os.path.isdir(item):
                # 월 + 주차 패턴 확인 (예: 8월3주차, 8월4주차)
                if re.match(r'\d+월\d+주차', item):
                    week_folders.append(item)
                    print(f"  ✅ 주차 폴더 발견: {item}")
    except Exception as e:
        print(f"❌ 폴더 검색 오류: {e}")
    
    return sorted(week_folders)

def get_target_week_folder():
    """대상 주차 폴더 결정"""
    week_folders = find_all_week_folders()
    
    if not week_folders:
        print("❌ 주차 폴더를 찾을 수 없습니다.")
        return None
    
    # 가장 최근 폴더 사용
    target_folder = week_folders[-1]
    print(f"🎯 대상 폴더: {target_folder}")
    return target_folder

def ensure_readme_exists(week_folder):
    """README.md 파일 존재 확인"""
    if not week_folder:
        return None
    
    readme_path = os.path.join(week_folder, 'README.md')
    
    print(f"🔍 README 파일 경로 확인: {readme_path}")
    print(f"🔍 파일 존재 여부: {os.path.exists(readme_path)}")
    
    if os.path.exists(readme_path):
        print(f"✅ README 파일 존재: {readme_path}")
        return readme_path
    
    print(f"❌ README.md 파일을 찾을 수 없습니다: {readme_path}")
    return None

def calculate_member_progress():
    """각 멤버별 진행률 계산 - 문제별 폴더 구조 대응"""
    week_folder = get_target_week_folder()
    
    if not week_folder:
        return {member: {'solved': 0, 'total': 0, 'percentage': 0, 'status': '📈'} for member in MEMBERS}
    
    member_stats = defaultdict(lambda: {'solved': 0, 'total': 0})
    
    try:
        # 주차 폴더 존재 확인
        if not os.path.exists(week_folder):
            print(f"❌ 주차 폴더가 존재하지 않습니다: {week_folder}")
            return {member: {'solved': 0, 'total': 0, 'percentage': 0, 'status': '📈'} for member in MEMBERS}
        
        items = os.listdir(week_folder)
        print(f"📅 {week_folder} 내용: {items}")
        
        # 날짜 폴더들 확인 (4자리 숫자: 0820, 0821 등)
        date_folders = [item for item in items if item.isdigit() and len(item) == 4]
        print(f"📅 날짜 폴더들: {date_folders}")
        
        for date_folder in date_folders:
            date_path = os.path.join(week_folder, date_folder)
            
            if os.path.isdir(date_path):
                print(f"📅 날짜 폴더 확인: {date_folder}")
                
                # 해당 날짜의 문제별 폴더들 찾기
                problem_folders = find_problem_folders(date_path)
                total_problems = len(problem_folders)
                
                print(f"   📁 문제 폴더들: {problem_folders}")
                print(f"   📝 총 문제 수: {total_problems}")
                
                # 각 멤버별 해결 현황 계산
                for member in MEMBERS:
                    solved_count = count_member_solved_problems(date_path, member, problem_folders)
                    
                    member_stats[member]['solved'] += solved_count
                    member_stats[member]['total'] += total_problems
                    
                    print(f"   👤 {member}: {solved_count}/{total_problems}개 해결")
                        
    except Exception as e:
        print(f"❌ 진행률 계산 오류: {e}")
        import traceback
        traceback.print_exc()
    
    # 진행률 계산 및 상태 결정
    progress = {}
    for member in MEMBERS:
        solved = member_stats[member]['solved']
        total = member_stats[member]['total']
        percentage = round((solved / total) * 100, 1) if total > 0 else 0
        
        # 상태 아이콘
        if percentage >= 90:
            status = "🔥"
        elif percentage >= 70:
            status = "⚡"
        elif percentage >= 50:
            status = "💪"
        else:
            status = "📈"
        
        progress[member] = {
            'solved': solved,
            'total': total,
            'percentage': percentage,
            'status': status
        }
    
    return progress

def find_problem_folders(date_path):
    """특정 날짜 경로에서 문제 폴더들 찾기"""
    problem_folders = []
    
    try:
        if not os.path.exists(date_path):
            return problem_folders
        
        items = os.listdir(date_path)
        
        for item in items:
            item_path = os.path.join(date_path, item)
            # 폴더이면서 문제 패턴 (BOJ_, PRO_ 등)에 맞는 것들
            if os.path.isdir(item_path) and (item.startswith('BOJ_') or item.startswith('PRO_')):
                problem_folders.append(item)
                
    except Exception as e:
        print(f"⚠️  문제 폴더 찾기 오류: {e}")
    
    return sorted(problem_folders)

def count_member_solved_problems(date_path, member, problem_folders):
    """특정 멤버가 해결한 문제 수 계산"""
    solved_count = 0
    
    try:
        for problem_folder in problem_folders:
            problem_path = os.path.join(date_path, problem_folder)
            
            if os.path.isdir(problem_path):
                # 문제 폴더 안의 파일들 확인
                files = os.listdir(problem_path)
                
                # 해당 멤버의 파일이 있는지 확인
                member_files = [f for f in files if member in f and f.endswith('.py')]
                
                if member_files:
                    solved_count += 1
                    print(f"     ✅ {member}: {problem_folder} 해결 ({member_files[0]})")
                    
    except Exception as e:
        print(f"⚠️  {member} 해결 문제 계산 오류: {e}")
    
    return solved_count

def generate_progress_section(progress):
    """진행률 섹션 생성"""
    lines = []
    lines.append("### 📊 참여자별 현황")
    lines.append("| 이름 | 해결 문제 | 진행률 | 상태 |")
    lines.append("|------|-----------|--------|------|")
    
    for member, data in progress.items():
        line = f"| {member} | {data['solved']}/{data['total']} | {data['percentage']}% | {data['status']} |"
        lines.append(line)
    
    # 전체 통계
    total_solved = sum(data['solved'] for data in progress.values())
    total_problems = sum(data['total'] for data in progress.values())
    avg_percentage = round(sum(data['percentage'] for data in progress.values()) / len(progress), 1) if progress else 0
    
    lines.append("")
    lines.append("### 📈 전체 통계")
    lines.append(f"- **총 해결 문제**: {total_solved}개")
    lines.append(f"- **평균 진행률**: {avg_percentage}%")
    lines.append(f"- **업데이트 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    return "\n".join(lines)

def update_readme_with_progress(progress):
    """README 파일 업데이트"""
    week_folder = get_target_week_folder()
    
    if not week_folder:
        print("❌ 대상 폴더를 찾을 수 없습니다.")
        return False
    
    # README 파일 존재 확인
    readme_path = ensure_readme_exists(week_folder)
    
    if not readme_path:
        print("❌ README 파일을 찾을 수 없습니다.")
        return False
    
    try:
        print(f"📖 README 파일 읽기 시도: {readme_path}")
        
        # 기존 내용 읽기
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ README 파일 읽기 성공 (길이: {len(content)} 문자)")
        
        # 새로운 진행률 섹션
        new_progress = generate_progress_section(progress)
        print(f"📊 새로운 진행률 섹션 생성 완료")
        
        # 기존 진행률 섹션 찾기 및 교체
        pattern = r'### 📊 참여자별 현황.*?(?=###|---|\Z)'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_progress, content, flags=re.DOTALL)
            print("🔄 기존 진행률 섹션 업데이트")
        else:
            # "## 📊 진행 현황" 섹션 찾아서 교체
            progress_pattern = r'## 📊 진행 현황.*?(?=##|---|\Z)'
            if re.search(progress_pattern, content, re.DOTALL):
                replacement = f"## 📊 진행 현황\n\n{new_progress}\n"
                content = re.sub(progress_pattern, replacement, content, flags=re.DOTALL)
                print("🔄 진행 현황 섹션 업데이트")
            else:
                content += f"\n\n---\n\n## 📊 진행 현황\n\n{new_progress}\n"
                print("➕ 새로운 진행률 섹션 추가")
        
        print(f"💾 README 파일 저장 시도: {readme_path}")
        
        # 파일 저장
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ README 업데이트 완료: {readme_path}")
        return True
        
    except Exception as e:
        print(f"❌ README 업데이트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def save_progress_log(progress):
    """진행률 로그 저장"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    today = datetime.now().strftime("%Y%m%d")
    log_data = {
        'date': today,
        'week_folder': get_target_week_folder(),
        'progress': progress,
        'timestamp': datetime.now().isoformat(),
        'file_structure_type': 'problem_folder_based'  # 새로운 구조 표시
    }
    
    log_file = os.path.join(log_dir, f"progress_log_{today}.json")
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        print(f"💾 로그 저장: {log_file}")
    except Exception as e:
        print(f"❌ 로그 저장 실패: {e}")

if __name__ == "__main__":
    print("📈 진행률 업데이트 시작! (문제별 폴더 구조)")
    
    try:
        # 현재 폴더 구조 확인
        print("🔍 현재 작업 디렉토리:", os.getcwd())
        print("🔍 현재 디렉토리 내용:", os.listdir('.'))
        
        week_folders = find_all_week_folders()
        target_folder = get_target_week_folder()
        
        print(f"🎯 발견된 주차 폴더들: {week_folders}")
        print(f"🎯 대상 폴더: {target_folder}")
        
        if target_folder:
            progress = calculate_member_progress()
            
            print("📊 계산된 진행률:")
            for member, data in progress.items():
                print(f"  {data['status']} {member}: {data['solved']}/{data['total']} ({data['percentage']}%)")
            
            # README 업데이트
            if update_readme_with_progress(progress):
                save_progress_log(progress)
                print("✅ 진행률 업데이트 완료!")
            else:
                print("❌ README 업데이트 실패")
        else:
            print("❌ 대상 폴더를 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()