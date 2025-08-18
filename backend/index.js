import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";

dotenv.config();

const app = express();
app.use(cors({ origin: process.env.FRONTEND_URL }))
app.use(express.json());

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

app.post("/api/analyze", async (req, res) => {
    console.log("api/analyze hit")
    const data=req.body;
    console.log(data);
    res.json(data);
    res.send(error);
});
app.get("/api/data", async (req, res) => {
    console.log("api/data hit")
  const { data, error } = await supabase
    .from("nurdd")
    .select("*")
    .order("timestamp", { ascending: false });
  if (error) return res.status(500).json({ error: error.message });
  console.log(data);
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
