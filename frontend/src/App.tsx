import React, { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Card,
  Stack,
  CircularProgress,
} from "@mui/material";

import ReactMarkdown from "react-markdown";
import MdEditor from "react-markdown-editor-lite";
import "react-markdown-editor-lite/lib/index.css";
import html2pdf from "html2pdf.js";

// You can move this interface to a separate types file if you want
interface BrochureRequest {
  url: string;
  title?: string;
}

export default function BrochurePage() {
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");
  const [markdown, setMarkdown] = useState<string>("");
  const [summary, setSummary] = useState<string>("");
  const [loadingBrochure, setLoadingBrochure] = useState(false);
  const [loadingSummary, setLoadingSummary] = useState(false);

  // Generate Brochure Markdown
  const handleGenerateBrochure = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingBrochure(true);
    setMarkdown("");
    const body: BrochureRequest = { url, title };
    const resp = await fetch("http://127.0.0.1:8000/brochure", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await resp.json();
    setMarkdown(data.markdown);
    setLoadingBrochure(false);
  };

  // Get Summary
  const handleShowSummary = async () => {
    setLoadingSummary(true);
    const resp = await fetch("http://127.0.0.1:8000/summarise", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await resp.json();
    setSummary(data.summary);
    setLoadingSummary(false);
  };

  // PDF Download from Markdown preview
  const handleDownloadPDF = () => {
    const element = document.getElementById("markdown-preview");
    if (element) {
      html2pdf().from(element).save("brochure.pdf");
    }
  };

  return (
    <Stack
      sx={{
        minHeight: "100vh",
        minInlineSize: "100vw",
        justifyContent: "center",
        alignItems: "center",
        background: "#fff",
      }}
    >
      <Stack justifyContent="center">
        <Typography variant="h4" fontWeight={700} mb={3} align="center">
          Website Brochure Generator
        </Typography>
        <Card
          sx={{
            p: 3,
            mb: 4,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <form onSubmit={handleGenerateBrochure} style={{ width: "100%" }}>
            <Stack spacing={2} alignItems="center" sx={{ width: "100%" }}>
              <TextField
                label="Website URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                sx={{ maxWidth: 400, width: "100%" }}
              />
              <TextField
                label="Company Name (optional)"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                sx={{ maxWidth: 400, width: "100%" }}
              />
              <Button
                type="submit"
                variant="contained"
                disabled={loadingBrochure || !url}
                sx={{ maxWidth: 400, width: "100%" }}
              >
                {loadingBrochure ? <CircularProgress size={20} /> : "Generate"}
              </Button>
              <Button
                onClick={handleShowSummary}
                variant="outlined"
                disabled={loadingSummary || !url}
                sx={{ maxWidth: 400, width: "100%" }}
              >
                {loadingSummary ? (
                  <CircularProgress size={16} />
                ) : (
                  "Show Summary"
                )}
              </Button>
            </Stack>
          </form>
        </Card>

        {summary && (
          <Card sx={{ mb: 3, p: 3, background: "#f5f5f7" }}>
            <Typography variant="h6" mb={1}>
              Summary
            </Typography>
            <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
              {summary}
            </Typography>
          </Card>
        )}

        {markdown && (
          <Card sx={{ mb: 4, p: 3 }}>
            <Typography variant="h6" mb={1}>
              Edit Brochure (Markdown)
            </Typography>
            <MdEditor
              value={markdown}
              style={{ height: "280px" }}
              onChange={({ text }) => setMarkdown(text)}
              renderHTML={(text) => <ReactMarkdown>{text}</ReactMarkdown>}
            />
            <Typography variant="h6" mt={3} mb={1}>
              Preview
            </Typography>
            <Box
              id="markdown-preview"
              sx={{
                border: "1px solid #eee",
                borderRadius: 2,
                p: 3,
                background: "#fff",
              }}
            >
              <ReactMarkdown>{markdown}</ReactMarkdown>
            </Box>
            <Button
              variant="contained"
              onClick={handleDownloadPDF}
              sx={{ mt: 3 }}
            >
              Download PDF
            </Button>
          </Card>
        )}
      </Stack>
    </Stack>
  );
}
