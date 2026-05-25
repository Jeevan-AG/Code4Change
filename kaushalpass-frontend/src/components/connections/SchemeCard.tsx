"use client";

import React from "react";
import { motion } from "framer-motion";
import { ShieldCheck, ChevronRight, FileText, CheckCircle2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface SchemeCardProps {
  title: string;
  description: string;
  eligibility: string;
  successRate: number;
  tags?: string[];
  isMatch?: boolean;
}

export function SchemeCard({ title, description, eligibility, successRate, tags = [], isMatch = true }: SchemeCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5 }}
      transition={{ duration: 0.4 }}
      className="relative w-full rounded-3xl p-[1px] overflow-hidden group"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/30 via-teal-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-white/5" />
      
      <div className="relative h-full bg-[#0B1120]/90 backdrop-blur-xl rounded-[23px] p-6 flex flex-col border border-white/10 shadow-2xl overflow-hidden">
        
        {/* Glow effect */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-emerald-500/20 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

        <div className="flex justify-between items-start mb-4 relative z-10">
          <div className="flex items-center gap-2">
            <div className="p-2.5 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
            </div>
            {isMatch && (
              <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-xs font-medium text-emerald-300 flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" />
                Strong Match
              </span>
            )}
          </div>
          <div className="flex flex-col items-end">
            <span className="text-3xl font-bold text-white tracking-tight">
              {successRate}%
            </span>
            <span className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">
              Success Rate
            </span>
          </div>
        </div>

        <h3 className="text-xl font-semibold text-white mb-2 leading-tight relative z-10">
          {title}
        </h3>
        <p className="text-sm text-slate-400 mb-6 line-clamp-2 relative z-10">
          {description}
        </p>

        <div className="mt-auto space-y-4 relative z-10">
          <div className="flex items-start gap-2 bg-slate-800/50 p-3 rounded-xl border border-white/5">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <p className="text-xs text-slate-300 font-medium leading-relaxed">
              <span className="text-amber-200">Eligibility:</span> {eligibility}
            </p>
          </div>

          {tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => (
                <span key={tag} className="px-2.5 py-1 bg-white/5 rounded-lg text-xs font-medium text-slate-300 border border-white/5">
                  {tag}
                </span>
              ))}
            </div>
          )}

          <button className="w-full mt-4 flex items-center justify-center gap-2 py-3.5 bg-white text-slate-900 rounded-xl font-semibold hover:bg-emerald-400 hover:text-white hover:shadow-[0_0_20px_rgba(52,211,153,0.3)] transition-all duration-300">
            <span>Apply Now</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
