import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";
import { spawn } from "child_process";
dotenv.config();

const app = express();
app.use(cors({ origin: process.env.FRONTEND_URL }))
app.use(express.json());

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);



app.post("/api/analyze", async (req, res) => {
  try {
    const { url } = req.body;
    console.log(req.body)

    if (!url || !/^https?:\/\/.+\..+/.test(url)) {
      return res.status(400).json({ error: "Invalid URL format" });
    }
    const python = spawn("python", ["scraper.py", url]);
    let dataString = "";

    python.stdout.on("data", (data) => {
      dataString += data.toString();
    });

    python.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
    });

    python.on("close", async (code) => {
      try {
        const result = JSON.parse(dataString);
        console.log(result)
        if (result.error) {
          return res.status(500).json({ error: result.error });
        }

        const { data, error } = await supabase
          .from("nurdd")
          .insert([{ url, brandname: result.brandname, description: result.description, timestamp: new Date().toISOString() }])
          .select();

        if (error) return res.status(500).json({ error: error.message });

        res.status(201).json(data[0]);
      } catch (err) {
        console.error("Parsing error:", err.message);
        res.status(500).json({ error: "Failed to parse scraper output" });
      }
    });
  } catch (err) {
    console.error("API error:", err.message);
    res.status(500).json({ error: "Internal server error" });
  }
});
app.get("/api/data", async (req, res) => {
    console.log("api/data hit")
  const { data, error } = await supabase
    .from("nurdd")
    .select("*")
    .order("timestamp", { ascending: false });
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});

app.put("/api/nurdd/:id", async (req, res) => {
  const { id } = req.params;
  const { description } = req.body;

  const { data, error } = await supabase
    .from("nurdd")
    .update({ description })
    .eq("id", id)
    .select();

  if (error) return res.status(500).json({ error: error.message });
  if (!data.length) return res.status(404).json({ error: "Website not found" });

  res.json(data[0]);
});

app.delete("/api/nurdd/:id", async (req, res) => {
  const { id } = req.params;

  const { data, error } = await supabase
    .from("nurdd")
    .delete()
    .eq("id", id)
    .select();

  if (error) return res.status(500).json({ error: error.message });
  if (!data.length) return res.status(404).json({ error: "Website not found" });

  res.json({ message: "Data deleted" });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
