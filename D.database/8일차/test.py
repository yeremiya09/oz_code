# 패키지 설치
# pip3 install timeit
# pip3 install BTrees

# 설치된 패키지 import
# from time import time
import time
from BTrees.IIBTree import IITreeSet

TABLE_SIZE = 320_000_000

# list (index (X) brute force)
# vs
# tree (index (O) tree search)

# 데이터 삽입 (INSERT)
# list
print("리스트 생성 시작")  # 로깅
start_time_list = time.time()
data_list = list(range(1, TABLE_SIZE))  # 데이터 생성
end_time_list = time.time()  # 시간 측정 종료
time_setup_list = end_time_list - start_time_list # 시간 계산
print(f'리스트 생성 소요 시간: {time_setup_list:.6f} sec')  # 로깅

# tree
print("트리 생성 시작")  # 로깅
start_time_tree = time.time()  # 시간 측정 시작
data_tree = IITreeSet(range(1, TABLE_SIZE))  # 데이터 생성
end_time_tree = time.time()  # 시간 측정 종료
time_setup_tree = end_time_tree - start_time_tree  # 시간 계산
print(f'트리 생성 소요 시간: {time_setup_tree:.6f} sec')  # 로깅


# 데이터 조회 (SELECT)
# list
def fetch_from_list(target):  # target: '개발자가 되고 싶습니다'
    for data in data_list:  # brute force 방식
        if data == target:
            return data


# tree
def fetch_from_tree(target):
    return data_tree.has_key(target)  # tree search 방식


target = 160_000_000


# list
print("리스트 조회 시작")  # 로깅
start_time_list = time.time()  # 시간 측정 시작
fetch_from_list(target)  # 데이터 조회
end_time_list = time.time()  # 시간 측정 종료
time_fetch_list = end_time_list - start_time_list  # 시간 계산
print(f'리스트 조회 소요 시간: {time_fetch_list:.6f} sec')  # 로깅

# tree
print("트리 조회 시작")  # 로깅
start_time_tree = time.time()  # 시간 측정 시작
fetch_from_tree(target)  # 데이터 조회
end_time_tree = time.time()  # 시간 측정 종료
time_fetch_tree = end_time_tree - start_time_tree  # 시간 계산
print(f'트리 조회 소요 시간: {time_fetch_tree:.6f} sec')  # 로깅