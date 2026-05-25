"use client";

import React from "react";
import { motion } from "framer-motion";
import { Briefcase, MapPin, DollarSign, ChevronRight, Star } from "lucide-react";

interface JobOpportunityCardProps {
  title: string;
  company: string;
  location: string;
  salary: string;
  matchScore: number;
  type: string; // e.g. "Full-time", "Contract"
}

export function JobOpportunityCard({ title, company, location, salary, matchScore, type }: JobOpportunityCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.3 }}
      className="relative w-full rounded-2xl p-[1px] overflow-hidden group cursor-pointer"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/30 via-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="absolute inset-0 bg-gradient-to-b from-white/10 to-transparent" />
      
      <div className="relative h-full bg-slate-900/80 backdrop-blur-md rounded-[15px] p-5 flex flex-col border border-white/10 hover:border-indigo-500/30 transition-colors">
        
        <div className="flex justify-between items-start mb-3">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Briefcase className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white leading-tight">{title}</h3>
              <p className="text-sm text-indigo-300 font-medium">{company}</p>
            </div>
          </div>
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-1 bg-indigo-500/20 px-2 py-1 rounded-lg border border-indigo-500/30">
              <Star className="w-3 h-3 text-indigo-400 fill-indigo-400" />
              <span className="text-xs font-bold text-indigo-200">{matchScore}% Match</span>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-3 my-4">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-white/5 px-2.5 py-1.5 rounded-md border border-white/5">
            <MapPin className="w-3.5 h-3.5" />
            {location}
          </div>
          <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-white/5 px-2.5 py-1.5 rounded-md border border-white/5">
            <DollarSign className="w-3.5 h-3.5" />
            {salary}
          </div>
          <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-white/5 px-2.5 py-1.5 rounded-md border border-white/5">
            <Briefcase className="w-3.5 h-3.5" />
            {type}
          </div>
        </div>

        <div className="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
          <span className="text-xs text-slate-500">Posted 2 days ago</span>
          <div className="flex items-center gap-1 text-sm font-semibold text-indigo-400 group-hover:text-indigo-300 transition-colors">
            View Details
            <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>

      </div>
    </motion.div>
  );
}
