import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { skills, experiences } from '../data/mockData';
import { User, Briefcase, Award, Calendar } from 'lucide-react';

const About = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 100
      }
    }
  };

  return (
    <div className="min-h-screen pt-20 pb-12">
      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="max-w-6xl mx-auto">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="text-center mb-16"
          >
            <motion.div variants={itemVariants}>
              <Badge variant="outline" className="mb-4 px-4 py-2 text-sm">
                <User className="w-4 h-4 mr-2" />
                About Me
              </Badge>
            </motion.div>
            <motion.h1
              variants={itemVariants}
              className="text-4xl md:text-5xl font-bold mb-6"
            >
              Passionate About{' '}
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Data & Innovation
              </span>
            </motion.h1>
            <motion.p
              variants={itemVariants}
              className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto leading-relaxed"
            >
              I'm a data analyst and developer with over 3 years of experience transforming 
              complex data into actionable insights. I specialize in building scalable analytics 
              solutions and interactive dashboards that drive business decisions.
            </motion.p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              variants={itemVariants}
              className="space-y-6"
            >
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <h3 className="text-2xl font-bold mb-4">My Journey</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  My passion for data began during my studies in computer science, where I 
                  discovered the power of turning raw information into meaningful insights. 
                  Over the years, I've worked with diverse teams to build data-driven solutions 
                  that have impacted business outcomes.
                </p>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  I believe in the intersection of technology and creativity, constantly 
                  learning new tools and techniques to solve complex problems. When I'm not 
                  coding or analyzing data, you'll find me exploring new visualization 
                  techniques or contributing to open-source projects.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                  <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-1">50+</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Dashboards Built</div>
                </div>
                <div className="text-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mb-1">1M+</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Data Points Analyzed</div>
                </div>
                <div className="text-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400 mb-1">25+</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">ML Models Deployed</div>
                </div>
                <div className="text-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                  <div className="text-2xl font-bold text-orange-600 dark:text-orange-400 mb-1">15+</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Satisfied Clients</div>
                </div>
              </div>
            </motion.div>

            <motion.div
              variants={itemVariants}
              className="relative"
            >
              <div className="aspect-square bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl p-8 text-white relative overflow-hidden">
                <div className="absolute inset-0 opacity-30" style={{
                  backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
                }} />
                <div className="relative z-10 h-full flex flex-col justify-center">
                  <div className="text-center">
                    <div className="text-6xl font-bold mb-4">3+</div>
                    <div className="text-xl mb-2">Years of Experience</div>
                    <div className="text-sm opacity-80">
                      Building data solutions that matter
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Technical <span className="text-blue-600 dark:text-blue-400">Expertise</span>
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              A comprehensive overview of my technical skills and proficiency levels
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {['Programming', 'Database', 'Visualization', 'Data Science'].map((category) => (
              <motion.div
                key={category}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                viewport={{ once: true }}
              >
                <Card className="p-6">
                  <CardHeader className="pb-4">
                    <CardTitle className="flex items-center space-x-2">
                      <Award className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <span>{category}</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {skills
                      .filter(skill => skill.category === category)
                      .map((skill) => (
                        <div key={skill.name} className="space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="font-medium">{skill.name}</span>
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                              {skill.level}%
                            </span>
                          </div>
                          <Progress value={skill.level} className="h-2" />
                        </div>
                      ))}
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Experience Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Professional <span className="text-blue-600 dark:text-blue-400">Experience</span>
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              My journey through different roles and organizations
            </p>
          </motion.div>

          <div className="space-y-8">
            {experiences.map((exp, index) => (
              <motion.div
                key={exp.id}
                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className={`flex flex-col ${index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'} gap-8 items-center`}
              >
                <div className="flex-1">
                  <Card className="p-6 hover:shadow-lg transition-shadow">
                    <CardContent className="p-0">
                      <div className="flex items-center space-x-2 mb-3">
                        <Briefcase className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                        <Badge variant="outline" className="text-sm">
                          <Calendar className="w-3 h-3 mr-1" />
                          {exp.period}
                        </Badge>
                      </div>
                      <h3 className="text-xl font-bold mb-2">{exp.title}</h3>
                      <p className="text-blue-600 dark:text-blue-400 font-medium mb-3">
                        {exp.company}
                      </p>
                      <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                        {exp.description}
                      </p>
                    </CardContent>
                  </Card>
                </div>
                <div className="flex-shrink-0 w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                  {index + 1}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Core <span className="text-blue-600 dark:text-blue-400">Values</span>
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              The principles that guide my work and decision-making
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "Data-Driven Decisions",
                description: "Every recommendation I make is backed by solid data analysis and statistical evidence.",
                icon: "📊"
              },
              {
                title: "Continuous Learning",
                description: "The tech landscape evolves rapidly, and I'm committed to staying current with new tools and techniques.",
                icon: "🚀"
              },
              {
                title: "Collaborative Approach",
                description: "The best solutions come from working closely with stakeholders to understand their needs.",
                icon: "🤝"
              }
            ].map((value, index) => (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <Card className="p-6 h-full hover:shadow-lg transition-shadow">
                  <CardContent className="p-0 text-center">
                    <div className="text-4xl mb-4">{value.icon}</div>
                    <h3 className="text-xl font-bold mb-3">{value.title}</h3>
                    <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                      {value.description}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;