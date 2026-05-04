"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Github,
  Mail,
  MapPin,
  ExternalLink,
  Code2,
  Layers,
  Palette,
  Zap,
  ArrowDown,
  Sparkles,
} from "lucide-react";

/* ─── animation variants ─── */
const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: "easeOut" },
  }),
};

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};

/* ─── data ─── */
const skills = [
  { name: "React", icon: Code2, color: "from-cyan-400 to-cyan-600" },
  { name: "TypeScript", icon: Code2, color: "from-blue-400 to-blue-600" },
  { name: "Next.js", icon: Zap, color: "from-gray-600 to-gray-900" },
  { name: "Tailwind CSS", icon: Palette, color: "from-teal-400 to-teal-600" },
  { name: "JavaScript", icon: Code2, color: "from-yellow-400 to-yellow-600" },
  { name: "HTML / CSS", icon: Layers, color: "from-orange-400 to-orange-600" },
];

const projects = [
  {
    title: "React UI Kit",
    description:
      "Reusable component library built with TypeScript and Storybook. Includes buttons, modals, cards, inputs, and more with full accessibility support.",
    tags: ["React", "TypeScript", "Storybook"],
    link: "https://ceps12.github.io/react-ui-kit/",
    github: "https://github.com/ceps12/react-ui-kit",
  },
  {
    title: "Crypto Dashboard",
    description:
      "Real-time cryptocurrency tracking dashboard with interactive charts, portfolio management, and price alerts using public API data.",
    tags: ["React", "Recharts", "REST API"],
    link: "https://ceps12.github.io/crypto-dashboard/",
    github: "https://github.com/ceps12/crypto-dashboard",
  },
  {
    title: "Task Manager",
    description:
      "Full-stack task management app with authentication, drag-and-drop boards, and real-time collaboration features.",
    tags: ["Next.js", "Firebase", "DnD Kit"],
    link: "#",
    github: "#",
  },
  {
    title: "CSS Animations",
    description:
      "Collection of 30+ beautiful CSS animations and hover effects. Pure CSS, no dependencies. A playground for creative web interactions.",
    tags: ["CSS", "Animation", "Creative"],
    link: "#",
    github: "#",
  },
];

/* ─── component ─── */
export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* ═══ NAV ═══ */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b"
      >
        <nav className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <a
            href="#"
            className="text-xl font-bold tracking-tight flex items-center gap-2"
          >
            <span className="text-primary">ceps</span>
            <span className="text-muted-foreground">12</span>
          </a>

          <div className="hidden sm:flex items-center gap-6 text-sm text-muted-foreground">
            <a href="#about" className="hover:text-foreground transition-colors">
              About
            </a>
            <a
              href="#skills"
              className="hover:text-foreground transition-colors"
            >
              Skills
            </a>
            <a
              href="#projects"
              className="hover:text-foreground transition-colors"
            >
              Projects
            </a>
            <a
              href="#contact"
              className="hover:text-foreground transition-colors"
            >
              Contact
            </a>
          </div>

          <div className="flex items-center gap-3">
            <a
              href="https://github.com/ceps12"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button variant="ghost" size="icon">
                <Github className="h-5 w-5" />
              </Button>
            </a>
            <a href="#contact">
              <Button size="sm" className="gap-2">
                <Mail className="h-4 w-4" />
                <span className="hidden sm:inline">Contact</span>
              </Button>
            </a>
          </div>
        </nav>
      </motion.header>

      <main className="flex-1">
        {/* ═══ HERO ═══ */}
        <section className="relative overflow-hidden">
          {/* background decoration */}
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-20 left-1/4 h-72 w-72 rounded-full bg-purple-200/40 blur-3xl" />
            <div className="absolute bottom-10 right-1/4 h-96 w-96 rounded-full bg-violet-200/30 blur-3xl" />
          </div>

          <div className="max-w-5xl mx-auto px-6 py-24 sm:py-32 lg:py-40">
            <motion.div
              variants={stagger}
              initial="hidden"
              animate="visible"
              className="max-w-2xl"
            >
              <motion.div variants={fadeUp} custom={0}>
                <Badge
                  variant="secondary"
                  className="mb-6 px-3 py-1 text-sm gap-1.5"
                >
                  <Sparkles className="h-3.5 w-3.5" />
                  Frontend Developer
                </Badge>
              </motion.div>

              <motion.h1
                variants={fadeUp}
                custom={1}
                className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.1] mb-6"
              >
                Building the web,{" "}
                <span className="bg-gradient-to-r from-purple-600 to-violet-500 bg-clip-text text-transparent">
                  one component
                </span>{" "}
                at a time.
              </motion.h1>

              <motion.p
                variants={fadeUp}
                custom={2}
                className="text-lg sm:text-xl text-muted-foreground leading-relaxed mb-8 max-w-xl"
              >
                Hi, I&apos;m{" "}
                <span className="text-foreground font-semibold">ceps12</span>.
                I craft modern, responsive web interfaces with React, TypeScript,
                and Next.js. Focused on clean code, pixel-perfect design, and
                great user experience.
              </motion.p>

              <motion.div
                variants={fadeUp}
                custom={3}
                className="flex flex-wrap gap-3"
              >
                <Button size="lg" className="gap-2" asChild>
                  <a href="#projects">
                    View Projects
                    <ArrowDown className="h-4 w-4" />
                  </a>
                </Button>
                <Button size="lg" variant="outline" className="gap-2" asChild>
                  <a
                    href="https://github.com/ceps12"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Github className="h-4 w-4" />
                    GitHub
                  </a>
                </Button>
              </motion.div>

              <motion.div
                variants={fadeUp}
                custom={4}
                className="mt-8 flex items-center gap-2 text-sm text-muted-foreground"
              >
                <MapPin className="h-4 w-4" />
                <span>Open to work &amp; collaboration</span>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* ═══ ABOUT ═══ */}
        <section id="about" className="py-20 sm:py-28">
          <div className="max-w-5xl mx-auto px-6">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={stagger}
            >
              <motion.h2
                variants={fadeUp}
                custom={0}
                className="text-3xl font-bold tracking-tight mb-4"
              >
                About Me
              </motion.h2>
              <motion.div
                variants={fadeUp}
                custom={1}
                className="w-12 h-1 bg-gradient-to-r from-purple-500 to-violet-500 rounded-full mb-8"
              />

              <div className="grid sm:grid-cols-2 gap-8">
                <motion.div variants={fadeUp} custom={2}>
                  <Card className="border-0 bg-muted/50">
                    <CardContent className="p-6">
                      <p className="text-muted-foreground leading-relaxed">
                        I&apos;m a frontend developer passionate about creating
                        clean, accessible, and performant web applications. I
                        enjoy turning complex problems into simple, beautiful
                        interfaces. My focus is on modern JavaScript frameworks
                        and the React ecosystem.
                      </p>
                    </CardContent>
                  </Card>
                </motion.div>
                <motion.div variants={fadeUp} custom={3}>
                  <Card className="border-0 bg-muted/50">
                    <CardContent className="p-6">
                      <p className="text-muted-foreground leading-relaxed">
                        I believe in writing clean, maintainable code and
                        following best practices. I&apos;m always learning new
                        technologies and improving my skills. Currently focused
                        on building production-ready applications with TypeScript
                        and Next.js.
                      </p>
                    </CardContent>
                  </Card>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </section>

        <Separator className="max-w-5xl mx-auto" />

        {/* ═══ SKILLS ═══ */}
        <section id="skills" className="py-20 sm:py-28">
          <div className="max-w-5xl mx-auto px-6">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={stagger}
            >
              <motion.h2
                variants={fadeUp}
                custom={0}
                className="text-3xl font-bold tracking-tight mb-4"
              >
                Skills & Technologies
              </motion.h2>
              <motion.div
                variants={fadeUp}
                custom={1}
                className="w-12 h-1 bg-gradient-to-r from-purple-500 to-violet-500 rounded-full mb-10"
              />

              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                {skills.map((skill, i) => (
                  <motion.div key={skill.name} variants={fadeUp} custom={i + 2}>
                    <Card className="group hover:shadow-md transition-all duration-300 border-0 hover:border-purple-200 dark:hover:border-purple-800 cursor-default h-full">
                      <CardContent className="p-5 flex flex-col items-center text-center gap-3">
                        <div
                          className={`h-12 w-12 rounded-xl bg-gradient-to-br ${skill.color} flex items-center justify-center shadow-sm`}
                        >
                          <skill.icon className="h-6 w-6 text-white" />
                        </div>
                        <span className="text-sm font-medium">
                          {skill.name}
                        </span>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </section>

        <Separator className="max-w-5xl mx-auto" />

        {/* ═══ PROJECTS ═══ */}
        <section id="projects" className="py-20 sm:py-28">
          <div className="max-w-5xl mx-auto px-6">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={stagger}
            >
              <motion.h2
                variants={fadeUp}
                custom={0}
                className="text-3xl font-bold tracking-tight mb-4"
              >
                Projects
              </motion.h2>
              <motion.div
                variants={fadeUp}
                custom={1}
                className="w-12 h-1 bg-gradient-to-r from-purple-500 to-violet-500 rounded-full mb-10"
              />

              <div className="grid sm:grid-cols-2 gap-6">
                {projects.map((project, i) => (
                  <motion.div key={project.title} variants={fadeUp} custom={i + 2}>
                    <Card className="group hover:shadow-lg transition-all duration-300 h-full flex flex-col">
                      <CardContent className="p-6 flex flex-col flex-1 gap-4">
                        {/* colored top bar */}
                        <div className="h-1.5 w-full rounded-full bg-gradient-to-r from-purple-400 to-violet-400" />

                        <h3 className="text-lg font-semibold group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                          {project.title}
                        </h3>

                        <p className="text-sm text-muted-foreground leading-relaxed flex-1">
                          {project.description}
                        </p>

                        <div className="flex flex-wrap gap-2 mt-auto">
                          {project.tags.map((tag) => (
                            <Badge
                              key={tag}
                              variant="secondary"
                              className="text-xs"
                            >
                              {tag}
                            </Badge>
                          ))}
                        </div>

                        <div className="flex gap-3 pt-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="gap-1.5 text-xs"
                            asChild
                          >
                            <a
                              href={project.github}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              <Github className="h-3.5 w-3.5" />
                              Code
                            </a>
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="gap-1.5 text-xs"
                            asChild
                          >
                            <a
                              href={project.link}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              <ExternalLink className="h-3.5 w-3.5" />
                              Demo
                            </a>
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </section>

        <Separator className="max-w-5xl mx-auto" />

        {/* ═══ CONTACT ═══ */}
        <section id="contact" className="py-20 sm:py-28">
          <div className="max-w-5xl mx-auto px-6">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={stagger}
              className="text-center"
            >
              <motion.h2
                variants={fadeUp}
                custom={0}
                className="text-3xl font-bold tracking-tight mb-4"
              >
                Get in Touch
              </motion.h2>
              <motion.div
                variants={fadeUp}
                custom={1}
                className="w-12 h-1 bg-gradient-to-r from-purple-500 to-violet-500 rounded-full mb-6 mx-auto"
              />
              <motion.p
                variants={fadeUp}
                custom={2}
                className="text-muted-foreground max-w-md mx-auto mb-10"
              >
                I&apos;m always open to discussing new projects, creative ideas,
                or opportunities to be part of your vision.
              </motion.p>

              <motion.div
                variants={fadeUp}
                custom={3}
                className="flex justify-center gap-4"
              >
                <Button
                  size="lg"
                  className="gap-2"
                  asChild
                >
                  <a href="mailto:ceps12@example.com">
                    <Mail className="h-4 w-4" />
                    Send Email
                  </a>
                </Button>
                <Button size="lg" variant="outline" className="gap-2" asChild>
                  <a
                    href="https://github.com/ceps12"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Github className="h-4 w-4" />
                    GitHub
                  </a>
                </Button>
              </motion.div>
            </motion.div>
          </div>
        </section>
      </main>

      {/* ═══ FOOTER ═══ */}
      <footer className="border-t py-8">
        <div className="max-w-5xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <p>
            &copy; {new Date().getFullYear()} ceps12. All rights reserved.
          </p>
          <p>Built with Next.js &amp; Tailwind CSS</p>
        </div>
      </footer>
    </div>
  );
}
