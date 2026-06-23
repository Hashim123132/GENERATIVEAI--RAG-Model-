import React, { useState } from "react";

export default function FileUpload({ onUploadComplete }: { onUploadComplete: () => void }) {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setMessage("Please select a PDF file.");
      return;
    }
    setUploading(true);
    setMessage("");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("/api/upload", { method: "POST", body: formData });
      const data = await res.json();
      setMessage(data.message || data.error || "Upload complete.");
      onUploadComplete();
    } catch {
      setMessage("Upload failed.");
    } finally {
      setUploading(false);
    }
    e.target.value = "";
  }

  return (
    <div className="file-upload">
      <label className="upload-btn">
        {uploading ? "Uploading..." : "Upload PDF"}
        <input type="file" accept=".pdf" onChange={handleFile} hidden disabled={uploading} />
      </label>
      {message && <span className="upload-msg">{message}</span>}
    </div>
  );
}
