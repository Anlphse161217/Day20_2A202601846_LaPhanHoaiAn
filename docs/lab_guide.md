# Lab Guide: Multi-Agent Research System

## Scenario

Bạn cần xây dựng một research assistant có thể nhận câu hỏi dài, tìm thông tin, phân tích và viết câu trả lời cuối cùng. Lab yêu cầu so sánh hai cách làm:

1. **Single-agent baseline**: một agent làm toàn bộ.
2. **Multi-agent workflow**: Supervisor điều phối Researcher, Analyst, Writer.

## Quy tắc quan trọng

- Không thêm agent nếu không có lý do rõ ràng.
- Mỗi agent phải có responsibility riêng.
- Shared state phải đủ rõ để debug.
- Phải có trace hoặc log cho từng bước.
- Phải benchmark, không chỉ nhìn output bằng cảm tính.

## Milestone 1: Baseline

File gợi ý:

- `src/multi_agent_research_lab/cli.py`
- `src/multi_agent_research_lab/services/llm_client.py`

TODO(student): thay baseline placeholder bằng một call LLM thật.

## Milestone 2: Supervisor

File gợi ý:

- `src/multi_agent_research_lab/agents/supervisor.py`
- `src/multi_agent_research_lab/graph/workflow.py`

TODO(student): implement routing policy.

Gợi ý câu hỏi thiết kế:

- Khi nào gọi Researcher?
- Khi nào gọi Analyst?
- Khi nào gọi Writer?
- Khi nào stop?
- Nếu agent fail thì retry hay fallback?

## Milestone 3: Worker agents

File gợi ý:

- `src/multi_agent_research_lab/agents/researcher.py`
- `src/multi_agent_research_lab/agents/analyst.py`
- `src/multi_agent_research_lab/agents/writer.py`

TODO(student): implement từng worker.

## Milestone 4: Trace và benchmark

File gợi ý:

- `src/multi_agent_research_lab/observability/tracing.py`
- `src/multi_agent_research_lab/evaluation/benchmark.py`
- `src/multi_agent_research_lab/evaluation/report.py`

Benchmark tối thiểu:

| Metric | Cách đo gợi ý |
|---|---|
| Latency | wall-clock time |
| Cost | token usage hoặc provider usage |
| Quality | rubric 0-10 do peer review |
| Citation coverage | số claims có source / tổng claims chính |
| Failure rate | số query fail / tổng query |

## Troubleshooting

### macOS: lỗi SSL certificate khi gọi API qua HTTPS (Tavily, OpenAI, ...)

Triệu chứng: khi implement `SearchClient` (hoặc bất kỳ HTTPS call nào) trên macOS, bạn có thể gặp lỗi kiểu:

```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
unable to get local issuer certificate
```

Nguyên nhân: Python cài từ python.org trên macOS **không dùng** certificate store của hệ điều hành, nên không tìm thấy CA bundle hợp lệ. Đây là lỗi môi trường, **không phải** do API key sai.

Cách khắc phục (chọn 1 trong 3):

1. **Chạy script cài certificate đi kèm Python** (nhanh nhất):

   ```bash
   /Applications/Python\ 3.12/Install\ Certificates.command
   ```

   (thay `3.12` bằng version Python của bạn)

2. **Dùng `certifi` trong code** — thêm `certifi` vào dependencies, rồi tạo SSL context khi gọi HTTPS:

   ```python
   import certifi
   import ssl
   from urllib.request import urlopen

   ssl_context = ssl.create_default_context(cafile=certifi.where())
   urlopen(request, timeout=timeout, context=ssl_context)
   ```

3. **Set biến môi trường** trỏ tới CA bundle của certifi (không cần đổi code):

   ```bash
   export SSL_CERT_FILE=$(python -m certifi)
   ```

## Exit ticket

Mỗi nhóm trả lời 2 câu:

1. Case nào nên dùng multi-agent? Vì sao?
- **Trường hợp NÊN dùng multi-agent:** Khi bài toán phức tạp, có nhiều workflow song song, cần các vai trò khác nhau (người viết, người tìm kiếm thông tin, người đánh giá) để giảm tỷ lệ sai sót (hallucination). Vì chia nhỏ vấn đề ra cho các agent chuyên biệt sẽ tăng chất lượng output.

2. Case nào không nên dùng multi-agent? Vì sao?
- **Trường hợp KHÔNG NÊN dùng multi-agent:** Khi task quá đơn giản (như tóm tắt 1 câu, phân tích cảm xúc) hoặc khi yêu cầu khắt khe về thời gian phản hồi (latency), chi phí thấp. Vì workflow multi-agent sinh ra số lượng token rất lớn và xử lý chậm hơn nhiều so với gọi 1 prompt thẳng.

## Phân tích Failure Mode & Cách Fix
- **Failure Mode thường gặp:** Agent Writer (hoặc Analyst) bị rơi vào vòng lặp vô hạn hoặc sinh ra nội dung bịa đặt (hallucination) khi SearchClient trả về kết quả rỗng hoặc không liên quan.
- **Cách Fix:** 
  1. Thêm một `CriticAgent` vào workflow để kiểm duyệt tính logic và nguồn trích dẫn của nội dung trước khi ra kết quả cuối cùng.
  2. Áp dụng cơ chế "Fallback" (nếu search fail 3 lần liên tiếp thì trả về câu trả lời mặc định là "Không tìm thấy thông tin").
  3. Cài đặt giới hạn số bước lặp (đã làm trong `supervisor.py` với `MAX_ITERATIONS`) để tránh tốn tiền API vô ích.
