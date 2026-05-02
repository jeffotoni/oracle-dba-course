package main

import (
	"bytes"
	"encoding/json"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
)

func TestPrintEndpoints(t *testing.T) {
	buf := new(bytes.Buffer)
	oldStdout := os.Stdout
	r, w, err := os.Pipe()
	if err != nil {
		t.Fatalf("pipe: %v", err)
	}
	os.Stdout = w

	printEndpoints(":8080")

	_ = w.Close()
	os.Stdout = oldStdout
	_, _ = buf.ReadFrom(r)

	output := buf.String()
	assertContains(t, output, "Servidor HTTP iniciado em :8080")
	assertContains(t, output, "GET    /health")
	assertContains(t, output, "POST   /api/v1/llm")
	assertContains(t, output, "DELETE /api/v1/llm?id=1")
}

func TestMethodNotAllowedByServeMux(t *testing.T) {
	application := &app{logger: slog.New(slog.NewTextHandler(bytes.NewBuffer(nil), nil))}
	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/v1/llm", application.handleGetLLMs)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/llm", nil)
	rec := httptest.NewRecorder()

	mux.ServeHTTP(rec, req)

	if rec.Code != http.StatusMethodNotAllowed {
		t.Fatalf("status esperado %d, recebido %d", http.StatusMethodNotAllowed, rec.Code)
	}
}

func TestCreateLLMInvalidJSON(t *testing.T) {
	application := &app{logger: slog.New(slog.NewTextHandler(bytes.NewBuffer(nil), nil))}
	req := httptest.NewRequest(http.MethodPost, "/api/v1/llm", bytes.NewBufferString(`{"nome":`))
	rec := httptest.NewRecorder()

	application.handleCreateLLM(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Fatalf("status esperado %d, recebido %d", http.StatusBadRequest, rec.Code)
	}
	assertJSONError(t, rec.Body.Bytes())
}

func TestCreateLLMValidation(t *testing.T) {
	application := &app{logger: slog.New(slog.NewTextHandler(bytes.NewBuffer(nil), nil))}
	body := bytes.NewBufferString(`{"nome":"","input_token_limit":0,"output_token_limit":0}`)
	req := httptest.NewRequest(http.MethodPost, "/api/v1/llm", body)
	rec := httptest.NewRecorder()

	application.handleCreateLLM(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Fatalf("status esperado %d, recebido %d", http.StatusBadRequest, rec.Code)
	}
	assertJSONError(t, rec.Body.Bytes())
}

func TestUpdateLLMRequiresID(t *testing.T) {
	application := &app{logger: slog.New(slog.NewTextHandler(bytes.NewBuffer(nil), nil))}
	body := bytes.NewBufferString(`{"nome":"gpt","input_token_limit":10,"output_token_limit":10}`)
	req := httptest.NewRequest(http.MethodPut, "/api/v1/llm", body)
	rec := httptest.NewRecorder()

	application.handleUpdateLLM(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Fatalf("status esperado %d, recebido %d", http.StatusBadRequest, rec.Code)
	}
	assertJSONError(t, rec.Body.Bytes())
}

func TestDeleteLLMInvalidID(t *testing.T) {
	application := &app{logger: slog.New(slog.NewTextHandler(bytes.NewBuffer(nil), nil))}
	req := httptest.NewRequest(http.MethodDelete, "/api/v1/llm?id=abc", nil)
	rec := httptest.NewRecorder()

	application.handleDeleteLLM(rec, req)

	if rec.Code != http.StatusBadRequest {
		t.Fatalf("status esperado %d, recebido %d", http.StatusBadRequest, rec.Code)
	}
	assertJSONError(t, rec.Body.Bytes())
}

func assertJSONError(t *testing.T, body []byte) {
	t.Helper()
	var response errorResponse
	if err := json.Unmarshal(body, &response); err != nil {
		t.Fatalf("resposta nao e json valido: %v", err)
	}
	if response.Error == "" {
		t.Fatal("campo error nao pode ser vazio")
	}
}

func assertContains(t *testing.T, value string, want string) {
	t.Helper()
	if !bytes.Contains([]byte(value), []byte(want)) {
		t.Fatalf("esperava encontrar %q em %q", want, value)
	}
}
