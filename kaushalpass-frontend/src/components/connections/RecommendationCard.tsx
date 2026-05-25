"use client";

import React from "react";
import { motion } from "framer-motion";
import { BookOpen, Award, ArrowRight, PlayCircle } from "lucide-react";

interface RecommendationCardProps {
  title: string;
  provider: string;
  duration: string;
  matchScore: number;
  type: "training" | "certification";
  thumbnailUrl?: string;
}

export function RecommendationCard({ title, provider, duration, matchScore, type, thumbnailUrl }: RecommendationCardProps) {
  const isTraining = type === "training";
  const iconColor = isTraining ? "text-indigo-400" : "text-emerald-400";
  const glowColor = isTraining ? "group-hover:shadow-indigo-500/20" : "group-hover:shadow-emerald-500/20";

  return (
    <motion.div 
      whileHover={{ y: -2 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="relative flex flex-col w-full rounded-2xl bg-[#111111] border border-white/[0.08] overflow-hidden group cursor-pointer transition-colors duration-300 hover:bg-[#161616]"
    >
      <div className="h-32 w-full relative overflow-hidden bg-white/[0.02] border-b border-white/[0.04]">
        {thumbnailUrl ? (
          <img src={thumbnailUrl} alt={title} className="w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-all duration-500" />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center opacity-20 group-hover:opacity-30 transition-opacity duration-300">
            {isTraining ? <BookOpen className="w-12 h-12 text-indigo-500" /> : <Award className="w-12 h-12 text-emerald-500" />}
          </div>
        )}
        
        {/* Subtle inner shadow overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#111111] to-transparent opacity-90" />

        <div className="absolute top-3 right-3 bg-black/60 backdrop-blur-md px-2.5 py-1 rounded-md border border-white/[0.08] flex items-center gap-1.5">
          <div className="w-1 h-1 rounded-full bg-emerald-400" />
          <span className="text-[10px] font-medium text-white uppercase tracking-wider">{matchScore}% Match</span>
        </div>
      </div>

      <div className="p-5 flex flex-col flex-1">
        <div className="flex items-center gap-2 mb-2.5">
          {isTraining ? <BookOpen className={`w-3.5 h-3.5 ${iconColor}`} /> : <Award className={`w-3.5 h-3.5 ${iconColor}`} />}
          <span className="text-[10px] font-medium text-neutral-400 uppercase tracking-wider">{type}</span>
        </div>
        
        <h3 className="text-base font-medium text-white mb-1.5 line-clamp-2 leading-snug tracking-tight">{title}</h3>
        <p className="text-sm text-neutral-400 mb-6">{provider}</p>

        <div className="mt-auto flex items-center justify-between border-t border-white/[0.06] pt-4">
          <div className="flex flex-col gap-0.5">
            <span className="text-[10px] text-neutral-500 uppercase tracking-wider font-medium">Duration</span>
            <span className="text-xs font-medium text-neutral-300">{duration}</span>
          </div>
          
          <button className={`flex items-center justify-center w-8 h-8 rounded-full bg-white/[0.04] border border-white/[0.08] group-hover:bg-white/[0.08] transition-all ${glowColor}`}>
            {isTraining ? (
              <PlayCircle className={`w-4 h-4 ${iconColor}`} />
            ) : (
              <ArrowRight className={`w-4 h-4 ${iconColor} group-hover:translate-x-0.5 transition-transform`} />
            )}
          </button>
        </div>
      </div>
    </motion.div>
  );
}
