// quiz-app.js - UTME Quiz Interface Logic

// Question Data Parser
function parseQuestionFile(text, subject) {
    const questions = [];
    const lines = text.split('\n');
    let currentQuestion = null;
    let collectingExplanation = false;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // Match question number pattern (e.g., "1. " or "35. ")
        const questionMatch = line.match(/^(\d+)\.\s+(.+)$/);
        if (questionMatch) {
            // Save previous question if exists
            if (currentQuestion) {
                questions.push(currentQuestion);
            }
            
            // Start new question
            currentQuestion = {
                id: parseInt(questionMatch[1]),
                subject: subject,
                text: questionMatch[2],
                options: {},
                answer: null,
                explanation: null,
                exception: null
            };
            collectingExplanation = false;
            continue;
        }
        
        // Match options (A., B., C., D.)
        const optionMatch = line.match(/^([A-D])\.\s+(.+)$/);
        if (optionMatch && currentQuestion) {
            currentQuestion.options[optionMatch[1]] = optionMatch[2];
            continue;
        }
        
        // Match answer
        if (line.startsWith('Answer:') && currentQuestion) {
            currentQuestion.answer = line.replace('Answer:', '').trim();
            continue;
        }
        
        // Match explanation
        if (line.startsWith('Explanation:') && currentQuestion) {
            currentQuestion.explanation = line.replace('Explanation:', '').trim();
            collectingExplanation = true;
            continue;
        }
        
        // Match exception
        if (line.startsWith('Exception:') && currentQuestion) {
            currentQuestion.exception = line.replace('Exception:', '').trim();
            collectingExplanation = false;
            continue;
        }
        
        // Continue collecting explanation if we're in explanation mode
        if (collectingExplanation && line && currentQuestion) {
            currentQuestion.explanation += ' ' + line;
        }
    }
    
    // Don't forget the last question
    if (currentQuestion) {
        questions.push(currentQuestion);
    }
    
    return questions;
}

// Sample questions (in production, load from files)
const sampleQuestions = [
    {
        id: 1,
        subject: 'Physics',
        text: 'A body moving with constant velocity has:',
        options: {
            'A': 'Zero acceleration',
            'B': 'Constant acceleration',
            'C': 'Increasing acceleration',
            'D': 'Decreasing acceleration'
        },
        answer: 'A',
        explanation: 'Constant velocity means no change in speed or direction, so a = Δv/Δt = 0.',
        exception: 'Many confuse velocity with speed; constant speed with changing direction (circular motion) HAS acceleration.'
    },
    {
        id: 2,
        subject: 'Physics',
        text: 'An object is thrown vertically upward. At its highest point:',
        options: {
            'A': 'Velocity = 0, acceleration = 0',
            'B': 'Velocity = 0, acceleration = g (downward)',
            'C': 'Velocity = g, acceleration = 0',
            'D': 'Both velocity and acceleration are maximum'
        },
        answer: 'B',
        explanation: 'At peak, v = 0 instantaneously, but gravity still acts (a = 9.8 m/s² downward).',
        exception: 'Acceleration is NOT zero at highest point—common misconception; gravity never stops acting.'
    }
    // Add more questions as needed
];

// Quiz State Management
class QuizState {
    constructor(questions, duration = 900) { // 15 minutes default
        this.questions = questions;
        this.duration = duration; // in seconds
        this.timeRemaining = duration;
        this.currentQuestionIndex = 0;
        this.userAnswers = {}; // { questionId: selectedOption }
        this.flaggedQuestions = new Set();
        this.startTime = Date.now();
        this.timerInterval = null;
        this.isSubmitted = false;
    }
    
    getCurrentQuestion() {
        return this.questions[this.currentQuestionIndex];
    }
    
    setAnswer(questionId, option) {
        this.userAnswers[questionId] = option;
    }
    
    getAnswer(questionId) {
        return this.userAnswers[questionId];
    }
    
    clearAnswer(questionId) {
        delete this.userAnswers[questionId];
    }
    
    toggleFlag(questionId) {
        if (this.flaggedQuestions.has(questionId)) {
            this.flaggedQuestions.delete(questionId);
        } else {
            this.flaggedQuestions.add(questionId);
        }
    }
    
    isFlagged(questionId) {
        return this.flaggedQuestions.has(questionId);
    }
    
    goToQuestion(index) {
        if (index >= 0 && index < this.questions.length) {
            this.currentQuestionIndex = index;
            return true;
        }
        return false;
    }
    
    nextQuestion() {
        if (this.currentQuestionIndex < this.questions.length - 1) {
            this.currentQuestionIndex++;
            return true;
        }
        return false;
    }
    
    prevQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            return true;
        }
        return false;
    }
    
    getAnsweredCount() {
        return Object.keys(this.userAnswers).length;
    }
    
    getUnansweredCount() {
        return this.questions.length - this.getAnsweredCount();
    }
    
    getFlaggedCount() {
        return this.flaggedQuestions.size;
    }
    
    getScore() {
        let correct = 0;
        for (const question of this.questions) {
            if (this.userAnswers[question.id] === question.answer) {
                correct++;
            }
        }
        return {
            correct,
            total: this.questions.length,
            percentage: (correct / this.questions.length) * 100
        };
    }
    
    startTimer(onTick, onComplete) {
        this.timerInterval = setInterval(() => {
            this.timeRemaining--;
            
            if (onTick) {
                onTick(this.timeRemaining);
            }
            
            if (this.timeRemaining <= 0) {
                this.stopTimer();
                if (onComplete) {
                    onComplete();
                }
            }
        }, 1000);
    }
    
    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
    
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
}

// UI Controller
class QuizUI {
    constructor(quizState) {
        this.state = quizState;
        this.elements = this.cacheElements();
        this.attachEventListeners();
        this.render();
        this.startTimer();
    }
    
    cacheElements() {
        return {
            // Header
            subjectName: document.getElementById('subjectName'),
            currentQuestionNum: document.getElementById('currentQuestionNum'),
            totalQuestions: document.getElementById('totalQuestions'),
            timerDisplay: document.getElementById('timerDisplay'),
            timerProgressCircle: document.getElementById('timerProgressCircle'),
            
            // Sidebar
            sidebar: document.getElementById('quizSidebar'),
            questionPalette: document.getElementById('questionPalette'),
            answeredCount: document.getElementById('answeredCount'),
            unansweredCount: document.getElementById('unansweredCount'),
            flaggedCount: document.getElementById('flaggedCount'),
            
            // Main
            questionCard: document.getElementById('questionCard'),
            questionNumber: document.getElementById('questionNumber'),
            questionText: document.getElementById('questionText'),
            optionsContainer: document.getElementById('optionsContainer'),
            questionExplanation: document.getElementById('questionExplanation'),
            explanationContent: document.getElementById('explanationContent'),
            
            // Navigation
            prevBtn: document.getElementById('prevBtn'),
            nextBtn: document.getElementById('nextBtn'),
            clearBtn: document.getElementById('clearBtn'),
            flagBtn: document.getElementById('flagBtn'),
            
            // Buttons
            menuBtn: document.getElementById('menuBtn'),
            closeSidebar: document.getElementById('closeSidebar'),
            mobilePaletteBtn: document.getElementById('mobilePaletteBtn'),
            submitBtn: document.getElementById('submitBtn'),
            calculatorBtn: document.getElementById('calculatorBtn'),
            
            // Modals
            submitModal: document.getElementById('submitModal'),
            closeSubmitModal: document.getElementById('closeSubmitModal'),
            cancelSubmitBtn: document.getElementById('cancelSubmitBtn'),
            confirmSubmitBtn: document.getElementById('confirmSubmitBtn'),
            calculatorModal: document.getElementById('calculatorModal'),
            closeCalculatorModal: document.getElementById('closeCalculatorModal'),
            timeUpModal: document.getElementById('timeUpModal'),
            viewResultsBtn: document.getElementById('viewResultsBtn')
        };
    }
    
    attachEventListeners() {
        // Navigation
        this.elements.prevBtn.addEventListener('click', () => this.handlePrevious());
        this.elements.nextBtn.addEventListener('click', () => this.handleNext());
        this.elements.clearBtn.addEventListener('click', () => this.handleClearAnswer());
        this.elements.flagBtn.addEventListener('click', () => this.handleToggleFlag());
        
        // Sidebar
        this.elements.menuBtn.addEventListener('click', () => this.toggleSidebar());
        this.elements.closeSidebar.addEventListener('click', () => this.toggleSidebar());
        this.elements.mobilePaletteBtn.addEventListener('click', () => this.toggleSidebar());
        
        // Submit
        this.elements.submitBtn.addEventListener('click', () => this.showSubmitModal());
        this.elements.closeSubmitModal.addEventListener('click', () => this.hideSubmitModal());
        this.elements.cancelSubmitBtn.addEventListener('click', () => this.hideSubmitModal());
        this.elements.confirmSubmitBtn.addEventListener('click', () => this.handleSubmit());
        
        // Calculator
        this.elements.calculatorBtn.addEventListener('click', () => this.showCalculatorModal());
        this.elements.closeCalculatorModal.addEventListener('click', () => this.hideCalculatorModal());
        
        // Calculator buttons
        document.querySelectorAll('.calc-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleCalculator(e));
        });
        
        // View results
        this.elements.viewResultsBtn.addEventListener('click', () => this.showResults());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }
    
    render() {
        this.renderHeader();
        this.renderQuestionPalette();
        this.renderQuestion();
        this.renderStats();
    }
    
    renderHeader() {
        const question = this.state.getCurrentQuestion();
        this.elements.subjectName.textContent = question.subject;
        this.elements.currentQuestionNum.textContent = this.state.currentQuestionIndex + 1;
        this.elements.totalQuestions.textContent = this.state.questions.length;
    }
    
    renderQuestionPalette() {
        this.elements.questionPalette.innerHTML = '';
        
        this.state.questions.forEach((question, index) => {
            const btn = document.createElement('button');
            btn.className = 'palette-btn';
            btn.textContent = index + 1;
            
            // Add status classes
            if (index === this.state.currentQuestionIndex) {
                btn.classList.add('current');
            } else if (this.state.getAnswer(question.id)) {
                btn.classList.add('answered');
            }
            
            if (this.state.isFlagged(question.id)) {
                btn.classList.add('flagged');
            }
            
            btn.addEventListener('click', () => {
                this.state.goToQuestion(index);
                this.render();
                this.closeSidebarOnMobile();
            });
            
            this.elements.questionPalette.appendChild(btn);
        });
    }
    
    renderQuestion() {
        const question = this.state.getCurrentQuestion();

        // ── Passage panel ──────────────────────────────────────────────────
        // Re-use the existing panel when the passage is the same object so the
        // reader's scroll position is preserved while navigating within a group.
        // quiz-app.js detects identity by string equality (first 40 chars) as
        // documented in the HTML comments.
        const passageKey = question.passage ? question.passage.slice(0, 40) : null;
        let passagePanel = document.getElementById('passagePanel');

        if (question.passage) {
            if (!passagePanel) {
                passagePanel = document.createElement('div');
                passagePanel.id = 'passagePanel';
                passagePanel.style.cssText = [
                    'background:var(--surface-2,#1e1e2e)',
                    'border-left:4px solid var(--accent,#7c3aed)',
                    'border-radius:10px',
                    'padding:1.1rem 1.25rem',
                    'margin-bottom:1.1rem',
                    'max-height:260px',
                    'overflow-y:auto',
                    'scroll-behavior:smooth',
                ].join(';');
                // Insert before the question-header div (first child of questionCard)
                this.elements.questionCard.insertBefore(
                    passagePanel,
                    this.elements.questionCard.firstChild
                );
            }
            // Only rewrite innerHTML when the passage actually changes
            if (passagePanel.dataset.passageKey !== passageKey) {
                passagePanel.dataset.passageKey = passageKey;
                const title = question.passageTitle || 'Read the passage below';
                passagePanel.innerHTML =
                    `<div style="font-size:0.7rem;letter-spacing:.08em;text-transform:uppercase;` +
                    `color:var(--accent,#7c3aed);font-weight:700;margin-bottom:.6rem;">` +
                    `📄 ${title}</div>` +
                    `<div style="font-size:0.855rem;line-height:1.8;` +
                    `color:var(--text,#cdd6f4);white-space:pre-wrap;">${question.passage}</div>`;
                passagePanel.scrollTop = 0;
            }
        } else if (passagePanel) {
            // Question has no passage — remove panel entirely
            passagePanel.remove();
        }
        // ──────────────────────────────────────────────────────────────────

        // Update question number and text
        this.elements.questionNumber.textContent = this.state.currentQuestionIndex + 1;
        this.elements.questionText.textContent = question.text;
        
        // Render options
        this.elements.optionsContainer.innerHTML = '';
        const optionLabels = ['A', 'B', 'C', 'D'];
        
        optionLabels.forEach(label => {
            if (question.options[label]) {
                const option = document.createElement('div');
                option.className = 'option';
                
                const userAnswer = this.state.getAnswer(question.id);
                if (userAnswer === label) {
                    option.classList.add('selected');
                }
                
                option.innerHTML = `
                    <div class="option-label">${label}</div>
                    <div class="option-text">${question.options[label]}</div>
                `;
                
                option.addEventListener('click', () => this.handleSelectOption(label));
                
                this.elements.optionsContainer.appendChild(option);
            }
        });
        
        // Update flag button
        const isFlagged = this.state.isFlagged(question.id);
        if (isFlagged) {
            this.elements.flagBtn.classList.add('flagged');
            this.elements.flagBtn.querySelector('i').classList.remove('far');
            this.elements.flagBtn.querySelector('i').classList.add('fas');
        } else {
            this.elements.flagBtn.classList.remove('flagged');
            this.elements.flagBtn.querySelector('i').classList.remove('fas');
            this.elements.flagBtn.querySelector('i').classList.add('far');
        }
        
        // Update navigation buttons
        this.elements.prevBtn.disabled = this.state.currentQuestionIndex === 0;
        
        if (this.state.currentQuestionIndex === this.state.questions.length - 1) {
            this.elements.nextBtn.textContent = 'Submit';
            this.elements.nextBtn.innerHTML = '<i class="fas fa-check"></i> Review & Submit';
        } else {
            this.elements.nextBtn.innerHTML = 'Next <i class="fas fa-arrow-right"></i>';
        }
        
        // Scroll to top
        this.elements.questionCard.scrollTop = 0;
    }
    
    renderStats() {
        this.elements.answeredCount.textContent = this.state.getAnsweredCount();
        this.elements.unansweredCount.textContent = this.state.getUnansweredCount();
        this.elements.flaggedCount.textContent = this.state.getFlaggedCount();
    }
    
    startTimer() {
        this.state.startTimer(
            (timeRemaining) => this.updateTimer(timeRemaining),
            () => this.handleTimeUp()
        );
    }
    
    updateTimer(timeRemaining) {
        const formatted = this.state.formatTime(timeRemaining);
        this.elements.timerDisplay.textContent = formatted;
        
        // Update progress circle
        const progress = (timeRemaining / this.state.duration) * 163.36; // Circle circumference
        this.elements.timerProgressCircle.style.strokeDashoffset = 163.36 - progress;
        
        // Add warning/danger classes
        this.elements.timerDisplay.classList.remove('warning', 'danger');
        if (timeRemaining <= 300 && timeRemaining > 60) { // 5 minutes
            this.elements.timerDisplay.classList.add('warning');
        } else if (timeRemaining <= 60) { // 1 minute
            this.elements.timerDisplay.classList.add('danger');
        }
    }
    
    handleSelectOption(option) {
        const question = this.state.getCurrentQuestion();
        this.state.setAnswer(question.id, option);
        this.render();
    }
    
    handleClearAnswer() {
        const question = this.state.getCurrentQuestion();
        this.state.clearAnswer(question.id);
        this.render();
    }
    
    handleToggleFlag() {
        const question = this.state.getCurrentQuestion();
        this.state.toggleFlag(question.id);
        this.render();
    }
    
    handlePrevious() {
        if (this.state.prevQuestion()) {
            this.render();
        }
    }
    
    handleNext() {
        // If last question, show submit modal
        if (this.state.currentQuestionIndex === this.state.questions.length - 1) {
            this.showSubmitModal();
        } else if (this.state.nextQuestion()) {
            this.render();
        }
    }
    
    handleKeyboard(e) {
        // Don't trigger shortcuts in modals or inputs
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }
        
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                this.handlePrevious();
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.handleNext();
                break;
            case 'a':
            case 'A':
                e.preventDefault();
                this.handleSelectOption('A');
                break;
            case 'b':
            case 'B':
                e.preventDefault();
                this.handleSelectOption('B');
                break;
            case 'c':
            case 'C':
                e.preventDefault();
                this.handleSelectOption('C');
                break;
            case 'd':
            case 'D':
                e.preventDefault();
                this.handleSelectOption('D');
                break;
            case 'f':
            case 'F':
                e.preventDefault();
                this.handleToggleFlag();
                break;
            case 'Escape':
                this.hideSubmitModal();
                this.hideCalculatorModal();
                break;
        }
    }
    
    toggleSidebar() {
        this.elements.sidebar.classList.toggle('open');
    }
    
    closeSidebarOnMobile() {
        if (window.innerWidth <= 1024) {
            this.elements.sidebar.classList.remove('open');
        }
    }
    
    showSubmitModal() {
        document.getElementById('modalTotalQuestions').textContent = this.state.questions.length;
        document.getElementById('modalAnsweredCount').textContent = this.state.getAnsweredCount();
        document.getElementById('modalUnansweredCount').textContent = this.state.getUnansweredCount();
        document.getElementById('modalTimeRemaining').textContent = this.state.formatTime(this.state.timeRemaining);
        
        this.elements.submitModal.classList.remove('hidden');
    }
    
    hideSubmitModal() {
        this.elements.submitModal.classList.add('hidden');
    }
    
    showCalculatorModal() {
        this.elements.calculatorModal.classList.remove('hidden');
    }
    
    hideCalculatorModal() {
        this.elements.calculatorModal.classList.add('hidden');
    }
    
    handleCalculator(e) {
        const btn = e.currentTarget;
        const display = document.getElementById('calcDisplay');
        const value = btn.dataset.value;
        const action = btn.dataset.action;
        
        if (value) {
            if (display.value === '0') {
                display.value = value;
            } else {
                display.value += value;
            }
        } else if (action) {
            switch(action) {
                case 'clear':
                    display.value = '0';
                    break;
                case 'delete':
                    display.value = display.value.slice(0, -1) || '0';
                    break;
                case 'add':
                case 'subtract':
                case 'multiply':
                case 'divide':
                    display.value += ' ' + btn.textContent + ' ';
                    break;
                case 'equals':
                    try {
                        const expr = display.value
                            .replace(/×/g, '*')
                            .replace(/÷/g, '/')
                            .replace(/−/g, '-');
                        display.value = eval(expr);
                    } catch {
                        display.value = 'Error';
                        setTimeout(() => display.value = '0', 1000);
                    }
                    break;
            }
        }
    }
    
    handleSubmit() {
        this.state.isSubmitted = true;
        this.state.stopTimer();
        this.hideSubmitModal();
        this.showResults();
    }
    
    handleTimeUp() {
        this.state.isSubmitted = true;
        this.state.stopTimer();
        // Hide time-up modal and go straight to results
        const timeUpModal = document.getElementById('timeUpModal');
        if (timeUpModal) timeUpModal.classList.add('hidden');
        this.showResults();
    }

    showResults() {
        const TOTAL_MARKS   = 400;
        const WRONG_PENALTY = 0.5;
        const marksPerQ     = TOTAL_MARKS / this.state.questions.length;

        let correct = 0, wrong = 0, skipped = 0;
        this.state.questions.forEach(q => {
            const ans = this.state.userAnswers[q.id];
            if (!ans)                  skipped++;
            else if (ans === q.answer) correct++;
            else                       wrong++;
        });

        const deductions = wrong * WRONG_PENALTY;
        const final      = Math.max(0, correct * marksPerQ - deductions);
        const finalStr   = final.toFixed(1);
        const pct        = ((final / TOTAL_MARKS) * 100).toFixed(1);
        const grade      = pct >= 70 ? 'EXCELLENT' : pct >= 55 ? 'GOOD' : pct >= 40 ? 'AVERAGE' : 'NEEDS WORK';
        const gradeColor = grade === 'EXCELLENT' ? '#4ade80' : grade === 'GOOD' ? '#a3e635' : grade === 'AVERAGE' ? '#facc15' : '#f87171';

        const elapsed  = Math.round((Date.now() - this.state.startTime) / 1000);
        const timeStr  = this.state.formatTime(elapsed);

        // Subject breakdown
        const subj = {};
        this.state.questions.forEach(q => {
            if (!subj[q.subject]) subj[q.subject] = { correct: 0, wrong: 0, skipped: 0, total: 0 };
            const ans = this.state.userAnswers[q.id];
            subj[q.subject].total++;
            if (!ans)                  subj[q.subject].skipped++;
            else if (ans === q.answer) subj[q.subject].correct++;
            else                       subj[q.subject].wrong++;
        });

        const statCard = (label, val, color) =>
            `<div style="background:var(--card,#131325);border:1px solid var(--border,#1e1e2e);border-radius:10px;padding:.85rem;text-align:center;">
                <div style="font-size:1.5rem;font-weight:700;color:${color}">${val}</div>
                <div style="font-size:.75rem;color:var(--muted,#64748b)">${label}</div>
            </div>`;

        const subjHTML = Object.entries(subj).map(([s, d]) => {
            const sp = d.total ? ((d.correct / d.total) * 100).toFixed(0) : 0;
            return `<div style="background:var(--card,#131325);border:1px solid var(--border,#1e1e2e);border-radius:10px;padding:1rem;">
                <div style="font-weight:600;margin-bottom:.4rem;font-size:.9rem;">${s}</div>
                <div style="font-size:.8rem;color:var(--muted,#64748b);">${d.correct}/${d.total} &nbsp;·&nbsp; ${sp}%</div>
                <div style="height:4px;background:var(--border,#1e1e2e);border-radius:2px;margin-top:.5rem;">
                    <div style="height:100%;width:${sp}%;background:var(--accent,#818cf8);border-radius:2px;"></div>
                </div>
            </div>`;
        }).join('');

        // Build overlay
        let overlay = document.getElementById('_grantResults');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = '_grantResults';
            document.body.appendChild(overlay);
        }
        overlay.style.cssText = 'position:fixed;inset:0;background:var(--bg,#0d0d1a);z-index:9999;overflow-y:auto;padding:2rem 1rem 5rem;color:var(--text,#e2e8f0);font-family:inherit;display:flex;flex-direction:column;align-items:center;';

        overlay.innerHTML = `
            <div style="width:100%;max-width:740px;">
                <div style="text-align:center;margin-bottom:2rem;">
                    <div style="font-size:.85rem;color:var(--muted,#64748b);margin-bottom:.3rem;">GrantApp AI · JAMB Practice</div>
                    <h1 style="font-size:1.6rem;font-weight:700;margin:0 0 .75rem;">Your Results</h1>
                    <div style="font-size:3.8rem;font-weight:800;color:var(--accent,#818cf8);line-height:1;">${finalStr}<span style="font-size:1.4rem;color:var(--muted,#64748b);"> / ${TOTAL_MARKS}</span></div>
                    <div style="margin:.6rem 0;font-size:1.05rem;">${pct}% &nbsp;·&nbsp; <span style="color:${gradeColor};font-weight:700;">${grade}</span></div>
                    <div style="font-size:.8rem;color:var(--muted,#64748b);">Time: ${timeStr} &nbsp;·&nbsp; −0.5 per wrong answer</div>
                </div>

                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin-bottom:1.5rem;">
                    ${statCard('Correct', correct, '#4ade80')}
                    ${statCard('Wrong', wrong, '#f87171')}
                    ${statCard('Skipped', skipped, '#94a3b8')}
                    ${statCard('Deducted', '−' + deductions.toFixed(1), '#fb923c')}
                </div>

                <h2 style="font-size:.9rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--muted,#64748b);margin-bottom:.75rem;">Subject Breakdown</h2>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.75rem;margin-bottom:1.5rem;">${subjHTML}</div>

                <div style="display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap;margin-bottom:1.5rem;">
                    <button id="_pdfBtn" style="background:var(--accent,#818cf8);color:#fff;border:none;border-radius:8px;padding:.7rem 1.8rem;font-size:.95rem;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:8px;">
                        <i class="fas fa-file-pdf"></i> Download PDF Report
                    </button>
                    <button id="_revBtn" style="background:transparent;color:var(--text,#e2e8f0);border:1px solid var(--border,#1e1e2e);border-radius:8px;padding:.7rem 1.8rem;font-size:.95rem;cursor:pointer;">
                        Review Answers
                    </button>
                </div>

                <div id="_revSection" style="display:none;">
                    <h2 style="font-size:.9rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--muted,#64748b);margin-bottom:.75rem;">Question Breakdown</h2>
                    <table style="width:100%;border-collapse:collapse;font-size:.82rem;">
                        <thead><tr style="color:var(--muted,#64748b);border-bottom:1px solid var(--border,#1e1e2e);">
                            <th style="padding:.4rem;text-align:left;width:2.5rem;">#</th>
                            <th style="padding:.4rem;text-align:left;">Question</th>
                            <th style="padding:.4rem;text-align:center;width:3.5rem;">Yours</th>
                            <th style="padding:.4rem;text-align:center;width:3.5rem;">Answer</th>
                        </tr></thead>
                        <tbody id="_revBody"></tbody>
                    </table>
                </div>
            </div>`;

        // Populate review table
        const tbody = document.getElementById('_revBody');
        this.state.questions.forEach((q, i) => {
            const ans   = this.state.userAnswers[q.id] || '—';
            const right = ans === q.answer;
            const skip  = ans === '—';
            const color = skip ? '#94a3b8' : right ? '#4ade80' : '#f87171';
            const icon  = skip ? '' : right ? '✓' : '✗';
            const shortQ = q.text.replace(/\n[\s\S]*/, '').substring(0, 85) + (q.text.length > 85 ? '…' : '');
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid var(--border,#1e1e2e)';
            if (!right && !skip) tr.style.background = 'rgba(248,113,113,.04)';
            tr.innerHTML = `
                <td style="padding:.4rem;color:var(--muted,#64748b)">${i + 1}</td>
                <td style="padding:.4rem;">
                    <div>${shortQ}</div>
                    ${!right && q.explanation ? `<div style="color:var(--muted,#64748b);font-size:.75rem;margin-top:2px;">Explanation: ${q.explanation}</div>` : ''}
                    ${!right && q.exception  ? `<div style="color:#fb923c;font-size:.75rem;">Note: ${q.exception}</div>` : ''}
                </td>
                <td style="padding:.4rem;text-align:center;color:${color};font-weight:700;">${ans} ${icon}</td>
                <td style="padding:.4rem;text-align:center;color:#4ade80;font-weight:700;">${q.answer}</td>`;
            tbody.appendChild(tr);
        });

        document.getElementById('_revBtn').onclick = function () {
            const s = document.getElementById('_revSection');
            const showing = s.style.display !== 'none';
            s.style.display = showing ? 'none' : 'block';
            this.textContent = showing ? 'Review Answers' : 'Hide Review';
        };

        // Capture state for PDF closure
        const stateSnapshot = {
            questions: this.state.questions,
            userAnswers: { ...this.state.userAnswers }
        };
        document.getElementById('_pdfBtn').onclick = () =>
            this._generatePDF(stateSnapshot, finalStr, pct, grade, gradeColor, correct, wrong, skipped, deductions, timeStr, subj, TOTAL_MARKS);
    }

    _generatePDF(state, finalStr, pct, grade, gradeColor, correct, wrong, skipped, deductions, timeStr, subj, TOTAL_MARKS) {
        if (!window.jspdf) {
            alert('PDF library not loaded — ensure jsPDF is included in the page.');
            return;
        }
        const { jsPDF } = window.jspdf;
        const doc   = new jsPDF({ unit: 'pt', format: 'a4' });
        const W     = doc.internal.pageSize.getWidth();
        const H     = doc.internal.pageSize.getHeight();
        const M     = 40;
        const today = new Date().toISOString().split('T')[0];
        let y = M;

        const np = (need) => { if (y + need > H - M) { doc.addPage(); y = M; } };

        // ── Header bar ──
        doc.setFillColor(13, 13, 26);
        doc.rect(0, 0, W, 58, 'F');
        doc.setTextColor(129, 140, 248); doc.setFontSize(15); doc.setFont('helvetica', 'bold');
        doc.text('GrantApp AI', M, 36);
        doc.setTextColor(100, 116, 139); doc.setFontSize(8.5); doc.setFont('helvetica', 'normal');
        doc.text(`JAMB Practice Test Results — ${today}`, M, 50);
        y = 76;

        // ── Score ──
        doc.setTextColor(129, 140, 248); doc.setFontSize(34); doc.setFont('helvetica', 'bold');
        doc.text(`${pct}%`, W / 2, y + 8, { align: 'center' }); y += 18;
        doc.setFontSize(11); doc.setTextColor(200, 200, 220);
        doc.text(`${finalStr} / ${TOTAL_MARKS}   Correct: ${correct}   Wrong: ${wrong}   Skipped: ${skipped}`, W / 2, y + 12, { align: 'center' }); y += 12;
        doc.setFontSize(9); doc.setTextColor(100, 116, 139);
        doc.text(`Deductions: −${deductions.toFixed(1)}   Negative marking: −0.5 per wrong   Time taken: ${timeStr}`, W / 2, y + 12, { align: 'center' }); y += 12;
        const gc = grade === 'EXCELLENT' ? [74, 222, 128] : grade === 'GOOD' ? [163, 230, 53] : grade === 'AVERAGE' ? [250, 204, 21] : [248, 113, 113];
        doc.setTextColor(...gc); doc.setFontSize(12); doc.setFont('helvetica', 'bold');
        doc.text(grade, W / 2, y + 16, { align: 'center' }); y += 28;

        // ── Divider ──
        doc.setDrawColor(30, 30, 46); doc.setLineWidth(0.5); doc.line(M, y, W - M, y); y += 12;

        // ── Subject breakdown ──
        doc.setTextColor(160, 170, 200); doc.setFontSize(9); doc.setFont('helvetica', 'bold');
        doc.text('SUBJECT BREAKDOWN', M, y); y += 11;
        doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5);
        Object.entries(subj).forEach(([s, d]) => {
            const sp = d.total ? ((d.correct / d.total) * 100).toFixed(1) : '0.0';
            doc.setTextColor(160, 170, 200);
            doc.text(`${s}:  ${d.correct}/${d.total} correct  (${sp}%)  ·  Wrong: ${d.wrong}  ·  Skipped: ${d.skipped}`, M, y); y += 12;
        }); y += 6;

        // ── Divider ──
        doc.line(M, y, W - M, y); y += 12;

        // ── Question breakdown ──
        doc.setTextColor(160, 170, 200); doc.setFontSize(9); doc.setFont('helvetica', 'bold');
        doc.text('QUESTION BREAKDOWN', M, y); y += 12;

        const CW   = W - M * 2;
        const cols = [26, CW - 26 - 40 - 40, 40, 40];
        const cx   = [M, M + 26, M + 26 + cols[1], M + 26 + cols[1] + 40];

        doc.setFillColor(20, 20, 38); doc.rect(M, y - 9, CW, 13, 'F');
        doc.setTextColor(100, 116, 139); doc.setFontSize(7.5); doc.setFont('helvetica', 'bold');
        ['#', 'QUESTION', 'YOURS', 'ANSWER'].forEach((h, i) => doc.text(h, cx[i] + 2, y)); y += 9;

        doc.setFont('helvetica', 'normal');
        state.questions.forEach((q, i) => {
            np(28);
            const ans   = state.userAnswers[q.id] || '—';
            const right = ans === q.answer;
            const skip  = ans === '—';
            const icon  = skip ? '' : right ? '✓' : '✗';

            if (!right && !skip) { doc.setFillColor(28, 10, 10); doc.rect(M, y - 9, CW, 12, 'F'); }

            const shortQ = q.text.replace(/\n[\s\S]*/, '').substring(0, 92) + (q.text.length > 92 ? '…' : '');
            doc.setTextColor(100, 116, 139); doc.setFontSize(7.5);
            doc.text(String(i + 1), cx[0] + 2, y);
            doc.setTextColor(190, 200, 215);
            doc.text(shortQ, cx[1] + 2, y, { maxWidth: cols[1] - 4 });
            const ac = skip ? [100, 116, 139] : right ? [74, 222, 128] : [248, 113, 113];
            doc.setTextColor(...ac); doc.text(`${ans} ${icon}`, cx[2] + 2, y);
            doc.setTextColor(74, 222, 128); doc.text(q.answer, cx[3] + 2, y); y += 12;

            if (!right && q.explanation) {
                np(18); doc.setTextColor(100, 116, 139); doc.setFontSize(7);
                const el = doc.splitTextToSize(`Explanation: ${q.explanation}`, cols[1] - 4);
                doc.text(el, cx[1] + 2, y); y += el.length * 8.5;
                if (q.exception) {
                    np(12); doc.setTextColor(251, 146, 60);
                    const nl = doc.splitTextToSize(`Note: ${q.exception}`, cols[1] - 4);
                    doc.text(nl, cx[1] + 2, y); y += nl.length * 8.5;
                }
            }
            doc.setDrawColor(18, 18, 32); doc.setLineWidth(0.3); doc.line(M, y - 1, W - M, y - 1);
        });

        // ── Page footers ──
        const pages = doc.internal.getNumberOfPages();
        for (let p = 1; p <= pages; p++) {
            doc.setPage(p); doc.setFontSize(7); doc.setTextColor(55, 55, 75);
            doc.text('GrantApp AI · 100 Days to UTME', M, H - 14);
            doc.text(`Page ${p} of ${pages}`, W - M, H - 14, { align: 'right' });
        }
        doc.save(`GrantApp_MEPC_${today}.pdf`);
    }
}

// Initialize Quiz
// QUESTIONS and DURATION are declared in the HTML's inline <script> — no loading, no routing.
document.addEventListener('DOMContentLoaded', () => {
    const quizState = new QuizState(QUESTIONS, typeof DURATION !== 'undefined' ? DURATION : 3600);
    const quizUI    = new QuizUI(quizState);

    window.addEventListener('beforeunload', (e) => {
        if (!quizState.isSubmitted) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
});
