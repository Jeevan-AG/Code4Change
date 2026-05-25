"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { SchemeCard } from "@/components/connections/SchemeCard";
import { JobOpportunityCard } from "@/components/connections/JobOpportunityCard";
import { RecommendationCard } from "@/components/connections/RecommendationCard";
import { 
  Sparkles, Bell, Search, SlidersHorizontal, 
  Layers, ShieldCheck, Briefcase, BookOpen, Activity 
} from "lucide-react";

const TABS = [
  { id: "all", label: "Overview", icon: Layers },
  { id: "schemes", label: "Gov. Schemes", icon: ShieldCheck },
  { id: "jobs", label: "Job Openings", icon: Briefcase },
  { id: "training", label: "Training & Certs", icon: BookOpen },
];

const mockSchemes = [
  {
    id: 1,
    title: "PM Vishwakarma Scheme",
    description: "End-to-end support for artisans and craftspeople to enhance quality, scale, and reach of their products.",
    eligibility: "Artisans working with hands/tools",
    successRate: 94,
    tags: ["Collateral-free", "Skill Upgradation", "Stipend"],
    isMatch: true,
  },
  {
    id: 2,
    title: "Mudra Yojana (PMMY)",
    description: "Loans up to ₹10 Lakhs for non-corporate, non-farm small/micro enterprises to start or expand business.",
    eligibility: "Any Indian Citizen, No defaults",
    successRate: 88,
    tags: ["Micro Credit", "Business Growth"],
    isMatch: true,
  }
];

const mockJobs = [
  {
    id: 1,
    title: "Senior Mehendi Artist",
    company: "Bridal Studio & Co.",
    location: "Mumbai, MH",
    salary: "₹25k - ₹35k /mo",
    matchScore: 92,
    type: "Full-time",
  },
  {
    id: 2,
    title: "Expert Tailor & Pattern Maker",
    company: "Urban Threads Boutique",
    location: "Remote",
    salary: "₹18k - ₹22k /mo",
    matchScore: 85,
    type: "Contract",
  }
];

const mockTraining = [
  {
    id: 1,
    title: "Advanced Boutique Management",
    provider: "NSDC Skill India",
    duration: "4 Weeks",
    matchScore: 96,
    type: "training" as const,
  },
  {
    id: 2,
    title: "Master Weaver Certification (NSQF Level 5)",
    provider: "Ministry of Textiles",
    duration: "Assessment Only",
    matchScore: 89,
    type: "certification" as const,
  }
];

export default function ConnectionsHub() {
  const [activeTab, setActiveTab] = useState("all");

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.05 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    show: { opacity: 1, y: 0, transition: { duration: 0.3 } }
  };

  return (
    <div className="min-h-screen bg-[#050505] relative overflow-hidden pb-32 text-slate-200 font-sans selection:bg-indigo-500/30">
      
      {/* Ultra-Premium Grid Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
        <div className="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-indigo-500/10 rounded-full blur-[120px] opacity-70" />
      </div>

      {/* Header - Clean, Precise, Functional */}
      <header className="sticky top-0 z-50 pt-6 pb-4 px-6 sm:px-10 transition-all bg-[#0A0A0A]/80 backdrop-blur-md border-b border-white/[0.06]">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer group">
            <div className="w-9 h-9 rounded-xl bg-white/[0.04] border border-white/[0.08] flex items-center justify-center group-hover:bg-white/[0.08] transition-colors">
              <Sparkles className="w-4 h-4 text-indigo-400" />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-white tracking-tight">KaushalLink</h1>
            </div>
          </div>

          <div className="flex items-center gap-5">
            <button className="relative text-neutral-400 hover:text-white transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-rose-500 rounded-full border border-[#0A0A0A]" />
            </button>
            <div className="w-9 h-9 rounded-full bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center cursor-pointer hover:bg-indigo-500/30 transition-colors text-indigo-300 font-medium text-sm">
              PR
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 sm:px-10 mt-10 relative z-10">
        
        {/* Welcome Section - Typography Focused, No Extreme Glass */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-12">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 mb-4">
              <Activity className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-medium text-emerald-400 tracking-wide">Level 4 Verified</span>
            </div>
            <h2 className="text-4xl font-medium text-white mb-3 tracking-tight">
              Opportunities for Priya
            </h2>
            <p className="text-neutral-400 text-lg leading-relaxed">
              Based on your verified <span className="text-neutral-200">Advanced Embroidery</span> skill, here are curated pathways with high success probabilities.
            </p>
          </div>
        </div>

        {/* Search & Filter - Professional and Understated */}
        <div className="flex flex-col sm:flex-row items-center gap-4 mb-10">
          <div className="relative flex-1 w-full group">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-neutral-500 group-focus-within:text-white transition-colors" />
            </div>
            <input 
              type="text" 
              placeholder="Search for schemes, jobs, or skills..." 
              className="w-full bg-[#111111] border border-white/[0.08] rounded-xl py-3 pl-11 pr-4 text-sm text-white placeholder-neutral-500 focus:outline-none focus:border-indigo-500/50 focus:bg-[#161616] transition-all shadow-sm"
            />
          </div>
          <button className="flex items-center gap-2 px-5 py-3 bg-white text-black rounded-xl hover:bg-neutral-200 transition-colors w-full sm:w-auto shrink-0 font-medium text-sm">
            <SlidersHorizontal className="w-4 h-4" />
            Filters
          </button>
        </div>

        {/* Tabs - Underlined Apple-style or Minimalist Vercel-style */}
        <div className="flex items-center gap-1 overflow-x-auto mb-8 border-b border-white/[0.06] scrollbar-hide pb-[-1px]">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors relative ${
                  isActive ? "text-white" : "text-neutral-500 hover:text-neutral-300"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-indigo-400" : ""}`} />
                {tab.label}
                {isActive && (
                  <motion.div 
                    layoutId="activeTabIndicator"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500"
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                )}
              </button>
            )
          })}
        </div>

        {/* Content Grid */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="show"
          key={activeTab} 
          className="space-y-12"
        >
          <AnimatePresence mode="popLayout">
            {(activeTab === "all" || activeTab === "schemes") && (
              <motion.section variants={itemVariants} layoutId="schemes-section">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-medium text-white tracking-tight">
                    Government Schemes
                  </h3>
                  <button className="text-sm font-medium text-indigo-400 hover:text-indigo-300 transition-colors">View all</button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  {mockSchemes.map((scheme) => (
                    <SchemeCard key={scheme.id} {...scheme} />
                  ))}
                </div>
              </motion.section>
            )}

            {(activeTab === "all" || activeTab === "jobs") && (
              <motion.section variants={itemVariants} layoutId="jobs-section">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-medium text-white tracking-tight">
                    Job Opportunities
                  </h3>
                  <button className="text-sm font-medium text-indigo-400 hover:text-indigo-300 transition-colors">View all</button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  {mockJobs.map((job) => (
                    <JobOpportunityCard key={job.id} {...job} />
                  ))}
                </div>
              </motion.section>
            )}

            {(activeTab === "all" || activeTab === "training") && (
              <motion.section variants={itemVariants} layoutId="training-section">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-medium text-white tracking-tight">
                    Training & Certifications
                  </h3>
                  <button className="text-sm font-medium text-indigo-400 hover:text-indigo-300 transition-colors">View all</button>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                  {mockTraining.map((training) => (
                    <RecommendationCard key={training.id} {...training} />
                  ))}
                </div>
              </motion.section>
            )}
          </AnimatePresence>
        </motion.div>

      </main>
    </div>
  );
}
