"use client";

import React from "react";
import { motion } from "framer-motion";
import { Sparkles, BellRing, Search, SlidersHorizontal, Layers, ShieldCheck, Briefcase, BookOpen, Activity, ArrowRight, PlayCircle } from "lucide-react";

interface IconProps {
  className?: string;
}

export function AnimatedSparkles({ className }: IconProps) {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
      className={className}
    >
      <motion.div
        animate={{ scale: [1, 1.2, 1] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      >
        <Sparkles className="w-full h-full" />
      </motion.div>
    </motion.div>
  );
}

export function AnimatedBell({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ rotate: [0, -15, 15, -15, 15, 0] }}
      transition={{ duration: 0.5, ease: "easeInOut" }}
      className={className}
    >
      <BellRing className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedSearch({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.1, rotate: 90 }}
      transition={{ type: "spring", stiffness: 300, damping: 10 }}
      className={className}
    >
      <Search className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedSliders({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ x: [0, -3, 3, -3, 0] }}
      transition={{ duration: 0.4 }}
      className={className}
    >
      <SlidersHorizontal className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedLayers({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ y: -3 }}
      className={className}
    >
      <Layers className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedShield({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.15 }}
      transition={{ type: "spring", stiffness: 400, damping: 10 }}
      className={className}
    >
      <ShieldCheck className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedBriefcase({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ y: -3, rotate: [-5, 5, 0] }}
      transition={{ duration: 0.3 }}
      className={className}
    >
      <Briefcase className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedBook({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.1, rotate: -5 }}
      transition={{ type: "spring", stiffness: 300, damping: 15 }}
      className={className}
    >
      <BookOpen className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedActivity({ className }: IconProps) {
  return (
    <motion.div
      animate={{ scale: [1, 1.15, 1], opacity: [0.8, 1, 0.8] }}
      transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
      className={className}
    >
      <Activity className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedArrowRight({ className }: IconProps) {
  return (
    <motion.div
      className={className}
      initial={{ x: 0 }}
      whileHover={{ x: 5 }}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
    >
      <ArrowRight className="w-full h-full" />
    </motion.div>
  );
}

export function AnimatedPlayCircle({ className }: IconProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: "spring", stiffness: 400, damping: 15 }}
      className={className}
    >
      <PlayCircle className="w-full h-full" />
    </motion.div>
  );
}
