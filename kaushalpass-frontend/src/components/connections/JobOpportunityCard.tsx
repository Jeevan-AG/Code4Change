"use client";

import React from "react";
import { motion, useMotionTemplate, useMotionValue } from "framer-motion";
import { Briefcase, MapPin, ArrowRight, Activity } from "lucide-react";

interface JobOpportunityCardProps {
  title: string;
  company: string;
  location: string;
  salary: string;
  matchScore: number;
  type: string;
}

export function JobOpportunityCard({ title, company, location, salary, matchScore, type }: JobOpportunityCardProps) {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  function handleMouseMove({ currentTarget, clientX, clientY }: React.MouseEvent) {
    const { left, top } = currentTarget.getBoundingClientRect();
    mouseX.set(clientX - left);
    mouseY.set(clientY - top);
  }

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ y: -2 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      onMouseMove={handleMouseMove}
      className="group relative flex flex-col rounded-2xl bg-[#111111] border border-white/[0.08] p-6 overflow-hidden cursor-pointer transition-colors duration-300"
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
      
      <div className="flex justify-between items-start mb-5 relative z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-white/[0.04] border border-white/[0.08] flex items-center justify-center group-hover:border-sky-500/20 group-hover:bg-sky-500/10 transition-colors duration-300">
            <Briefcase className="w-4 h-4 text-sky-400" />
          </div>
          <div>
            <h3 className="text-base font-medium text-white leading-tight tracking-tight">{title}</h3>
            <p className="text-sm text-neutral-400">{company}</p>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-2 mb-6 relative z-10">
        <div className="flex items-center justify-between p-2.5 rounded-lg bg-white/[0.03] border border-white/[0.04]">
          <div className="flex items-center gap-2">
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-[11px] text-neutral-300 font-medium tracking-wide uppercase">Match Score</span>
          </div>
          <span className="text-sm font-semibold text-emerald-400">{matchScore}%</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-6 relative z-10">
        <div className="flex flex-col gap-1">
          <span className="text-[10px] text-neutral-500 uppercase tracking-wider font-medium">Salary</span>
          <span className="text-sm text-neutral-200 font-medium">{salary}</span>
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-[10px] text-neutral-500 uppercase tracking-wider font-medium">Location</span>
          <div className="flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5 text-neutral-400" />
            <span className="text-sm text-neutral-200">{location}</span>
          </div>
        </div>
      </div>

      <div className="mt-auto pt-4 border-t border-white/[0.06] flex items-center justify-between relative z-10">
        <span className="px-2.5 py-1 bg-white/[0.04] rounded-md text-xs font-medium text-neutral-400 border border-white/[0.04]">
          {type}
        </span>
        <div className="flex items-center gap-1.5 text-sm font-medium text-neutral-400 group-hover:text-sky-400 transition-colors">
          View Details
          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </div>
      </div>

    </motion.div>
  );
}
