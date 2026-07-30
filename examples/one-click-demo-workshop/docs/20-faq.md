# ❓ 트러블슈팅 & 자주 묻는 질문 (FAQ)

## 🚨 트러블슈팅 가이드

### Q1. Ollama / LM Studio 연결 실패 (`Connection refused`)
- **원인**: 로컬 서버 프로세스가 실행되어 있지 않거나 포트 번호가 틀림.
- **해결**:
  - Ollama: 터미널에서 `ollama serve` 실행 여부 및 `http://localhost:11434` 접속 확인
  - LM Studio: `Developer` 탭에서 `Local Inference Server`가 `Started` 상태인지 확인 (포트: `1234`)

### Q2. Out of Memory (OOM) 또는 모델 로딩 실패
- **원인**: 메모리(RAM) 용량 초과.
- **해결**:
  - 8GB RAM 노트북인 경우 `gemma4:e2b` 이하의 소형 양자화 모델 사용.
  - 다른 리소스 점유 프로그램(웹 브라우저 탭, 다른 IDE) 종료.

### Q3. Windows PowerShell 보안 오류 (`Execution_Policies`)
- **원인**: PowerShell의 스크립트 실행 제약 정책.
- **해결**:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

---

## ❓ 자주 묻는 질문 (FAQ)

**Q: 행사 당일 인터넷 연결이 되지 않으면 어떡하나요?**  
A: 사전 안내에 따라 모델과 패키지를 사전 설치하셨다면 로컬 환경에서 100% 오프라인 동작 가능합니다.

**Q: Intel Mac 사용자인데 LM Studio에서 모델 생성이 느립니다.**  
A: Intel Mac 환경에서는 LM Studio 대신 Ollama CLI를 사용하는 편이 추론속도가 빠릅니다. `ollama run gemma4:e4b`로 테스트해보세요.
