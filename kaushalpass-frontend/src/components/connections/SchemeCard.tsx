"use client";

import React from "react";
import { motion, useMotionTemplate, useMotionValue } from "framer-motion";
import { ShieldCheck, ArrowRight, CheckCircle2 } from "lucide-react";

interface SchemeCardProps {
  title: string;
  description: string;
  eligibility: string;
  successRate: number;
  tags?: string[];
  isMatch?: boolean;
}

export function SchemeCard({ title, description, eligibility, successRate, tags = [], isMatch = true }: SchemeCardProps) {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  function handleMouseMove({ currentTarget, clientX, clientY }: React.MouseEvent) {
    const { left, top } = currentTarget.getBoundingClientRect();
    mouseX.set(clientX - left);
    mouseY.set(clientY - top);
  }

  return (
    <motion.div 
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -2 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      onMouseMove={handleMouseMove}
      className="group relative flex flex-col rounded-2xl bg-[#111111] border border-white/[0.08] p-6 overflow-hidden transition-colors duration-300"
    >
      <motion.div
        className="pointer-events-none absolute -inset-px rounded-2xl opacity-0 transition duration-300 group-hover:opacity-100"
        style={{
          background: useMotionTemplate`
            radial-gradient(
              300px circle at ${mouseX}px ${mouseY}px,
              rgba(255, 255, 255, 0.03),
              transparent 80%
            )
          `,
        }}
      />
      <motion.div
        className="pointer-events-none absolute -inset-px rounded-2xl opacity-0 transition duration-300 group-hover:opacity-100"
        style={{
          border: "1px solid",
          borderImageSource: useMotionTemplate`
            radial-gradient(
              150px circle at ${mouseX}px ${mouseY}px,
              rgba(255, 255, 255, 0.2),
              transparent 80%
            )
          `,
          borderImageSlice: 1,
        }}
      />

      <div className="flex justify-between items-start mb-5 relative z-10">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-white/[0.04] rounded-lg border border-white/[0.08] flex items-center justify-center group-hover:bg-indigo-500/10 group-hover:border-indigo-500/20 transition-colors duration-300">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
          </div>
          {isMatch && (
            <div className="flex items-center gap-1.5 px-2.5 py-0.5 bg-emerald-500/10 border border-emerald-500/20 rounded-md">
              <CheckCircle2 className="w-3 h-3 text-emerald-400" />
              <span className="text-[10px] font-medium text-emerald-400 uppercase tracking-wide">Top Match</span>
            </div>
          )}
        </div>
        <div className="flex flex-col items-end">
          <span className="text-2xl font-medium text-white tracking-tight">
            {successRate}<span className="text-sm text-neutral-500">%</span>
          </span>
          <span className="text-[10px] text-neutral-500 font-medium uppercase mt-0.5">
            Success
          </span>
        </div>
      </div>

      <h3 className="text-lg font-medium text-white mb-1.5 leading-tight tracking-tight relative z-10">
        {title}
      </h3>
      <p className="text-sm text-neutral-400 mb-5 line-clamp-2 leading-relaxed relative z-10">
        {description}
      </p>

      <div className="mt-auto space-y-5 relative z-10">
        <div className="flex flex-col gap-1">
          <span className="text-[10px] text-neutral-500 uppercase tracking-wider font-medium">Eligibility</span>
          <p className="text-sm text-neutral-300">
            {eligibility}
          </p>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {tags.map((tag) => (
            <span key={tag} className="px-2.5 py-1 bg-white/[0.04] rounded-md text-xs font-medium text-neutral-400 border border-white/[0.04] transition-colors">
              {tag}
            </span>
          ))}
        </div>

        <button className="w-full mt-2 group/btn flex items-center justify-between py-2.5 px-4 bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-white rounded-lg font-medium text-sm transition-all duration-200">
          <span>Apply via KaushalLink</span>
          <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
        </button>
      </div>
    </motion.div>
  );
}
