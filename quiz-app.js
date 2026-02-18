// quiz-app.js — GrantApp AI
// Zero fetching. Questions are defined as QUESTIONS[] in each quiz page.
// Duration is defined as DURATION (seconds) in each quiz page.

// ── Fisher-Yates Shuffle ─────────────────────────────────────
function shuffleQuestionOptions(questions) {
    return questions.map(q => {
        // Build array of option objects
        const opts = ['A','B','C','D']
            .filter(k => q.options[k] !== undefined && q.options[k] !== null && q.options[k] !== '')
            .map(k => ({ key: k, text: q.options[k] }));

        // Fisher-Yates shuffle
        for (let i = opts.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [opts[i], opts[j]] = [opts[j], opts[i]];
        }

        // Rebuild options with new A/B/C/D labels
        const newOptions = {};
        const labelMap   = {};  // old key → new label
        const labels = ['A','B','C','D'];
        opts.forEach((opt, idx) => {
            newOptions[labels[idx]] = opt.text;
            labelMap[opt.key] = labels[idx];
        });

        return {
            ...q,
            options: newOptions,
            answer: labelMap[q.answer]   // remap correct answer to new position
        };
    });
}

// ── Quiz State ──────────────────────────────────────────────
class QuizState {
    constructor(questions, duration) {
        this.questions             = shuffleQuestionOptions(questions);
        this.duration              = duration;
        this.timeRemaining         = duration;
        this.currentQuestionIndex  = 0;
        this.userAnswers           = {};       // { questionId: 'A'|'B'|'C'|'D' }
        this.flaggedQuestions      = new Set();
        this.timerInterval         = null;
        this.isSubmitted           = false;
    }

    getCurrentQuestion() { return this.questions[this.currentQuestionIndex]; }

    setAnswer(id, option)  { this.userAnswers[id] = option; }
    getAnswer(id)          { return this.userAnswers[id] || null; }
    clearAnswer(id)        { delete this.userAnswers[id]; }

    toggleFlag(id) {
        this.flaggedQuestions.has(id)
            ? this.flaggedQuestions.delete(id)
            : this.flaggedQuestions.add(id);
    }
    isFlagged(id) { return this.flaggedQuestions.has(id); }

    goToQuestion(i)  { if (i >= 0 && i < this.questions.length) { this.currentQuestionIndex = i; return true; } return false; }
    nextQuestion()   { return this.goToQuestion(this.currentQuestionIndex + 1); }
    prevQuestion()   { return this.goToQuestion(this.currentQuestionIndex - 1); }

    getAnsweredCount()   { return Object.keys(this.userAnswers).length; }
    getUnansweredCount() { return this.questions.length - this.getAnsweredCount(); }
    getFlaggedCount()    { return this.flaggedQuestions.size; }

    getScore() {
        let correct = 0;
        for (const q of this.questions) {
            if (this.userAnswers[q.id] === q.answer) correct++;
        }
        return { correct, total: this.questions.length, percentage: (correct / this.questions.length) * 100 };
    }

    formatTime(s) {
        const m = Math.floor(s / 60);
        const sec = s % 60;
        return `${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
    }

    startTimer(onTick, onComplete) {
        this.timerInterval = setInterval(() => {
            this.timeRemaining--;
            if (onTick) onTick(this.timeRemaining);
            if (this.timeRemaining <= 0) {
                this.stopTimer();
                if (onComplete) onComplete();
            }
        }, 1000);
    }

    stopTimer() {
        if (this.timerInterval) { clearInterval(this.timerInterval); this.timerInterval = null; }
    }
}

// ── Quiz UI ──────────────────────────────────────────────────
class QuizUI {
    constructor(state) {
        this.state = state;
        this.el    = this._cache();
        this._bind();
        this.render();
        this._startTimer();
    }

    _cache() {
        const g = id => document.getElementById(id);
        return {
            subjectName:          g('subjectName'),
            currentQuestionNum:   g('currentQuestionNum'),
            totalQuestions:       g('totalQuestions'),
            timerDisplay:         g('timerDisplay'),
            timerProgressCircle:  g('timerProgressCircle'),
            timerContainer:       g('quizTimerContainer'),

            sidebar:              g('quizSidebar'),
            questionPalette:      g('questionPalette'),
            answeredCount:        g('answeredCount'),
            unansweredCount:      g('unansweredCount'),
            flaggedCount:         g('flaggedCount'),

            questionNumber:       g('questionNumber'),
            questionText:         g('questionText'),
            optionsContainer:     g('optionsContainer'),
            questionExplanation:  g('questionExplanation'),
            explanationContent:   g('explanationContent'),

            prevBtn:              g('prevBtn'),
            nextBtn:              g('nextBtn'),
            clearBtn:             g('clearBtn'),
            flagBtn:              g('flagBtn'),

            menuBtn:              g('menuBtn'),
            closeSidebar:         g('closeSidebar'),
            mobilePaletteBtn:     g('mobilePaletteBtn'),
            submitBtn:            g('submitBtn'),
            calculatorBtn:        g('calculatorBtn'),

            submitModal:          g('submitModal'),
            closeSubmitModal:     g('closeSubmitModal'),
            cancelSubmitBtn:      g('cancelSubmitBtn'),
            confirmSubmitBtn:     g('confirmSubmitBtn'),
            calculatorModal:      g('calculatorModal'),
            closeCalculatorModal: g('closeCalculatorModal'),
            timeUpModal:          g('timeUpModal'),
            viewResultsBtn:       g('viewResultsBtn'),
        };
    }

    _bind() {
        const e = this.el;
        e.prevBtn.addEventListener('click',             () => this._prev());
        e.nextBtn.addEventListener('click',             () => this._next());
        e.clearBtn.addEventListener('click',            () => this._clearAnswer());
        e.flagBtn.addEventListener('click',             () => this._toggleFlag());
        e.menuBtn.addEventListener('click',             () => this._toggleSidebar());
        e.closeSidebar.addEventListener('click',        () => this._toggleSidebar());
        e.mobilePaletteBtn.addEventListener('click',    () => this._toggleSidebar());
        e.submitBtn.addEventListener('click',           () => this._showSubmitModal());
        e.closeSubmitModal.addEventListener('click',    () => this._hideSubmitModal());
        e.cancelSubmitBtn.addEventListener('click',     () => this._hideSubmitModal());
        e.confirmSubmitBtn.addEventListener('click',    () => this._submit());
        e.calculatorBtn.addEventListener('click',       () => this._showCalc());
        e.closeCalculatorModal.addEventListener('click',() => this._hideCalc());
        e.viewResultsBtn.addEventListener('click',      () => this._showResults());

        document.querySelectorAll('.calc-btn').forEach(btn =>
            btn.addEventListener('click', e => this._handleCalc(e))
        );

        document.addEventListener('keydown', e => this._keyboard(e));
    }

    // ── Render ──
    render() {
        this._renderHeader();
        this._renderPalette();
        this._renderQuestion();
        this._renderStats();
    }

    _renderHeader() {
        const q = this.state.getCurrentQuestion();
        this.el.subjectName.textContent        = q.subject;
        this.el.currentQuestionNum.textContent = this.state.currentQuestionIndex + 1;
        this.el.totalQuestions.textContent     = this.state.questions.length;
    }

    _renderPalette() {
        const palette = this.el.questionPalette;
        palette.innerHTML = '';
        this.state.questions.forEach((q, i) => {
            const btn = document.createElement('button');
            btn.className   = 'palette-btn';
            btn.textContent = i + 1;
            if (i === this.state.currentQuestionIndex)   btn.classList.add('current');
            else if (this.state.getAnswer(q.id))         btn.classList.add('answered');
            if (this.state.isFlagged(q.id))              btn.classList.add('flagged');
            btn.addEventListener('click', () => { this.state.goToQuestion(i); this.render(); this._closeSidebarMobile(); });
            palette.appendChild(btn);
        });
    }

    _renderQuestion() {
        const q = this.state.getCurrentQuestion();
        this.el.questionNumber.textContent = this.state.currentQuestionIndex + 1;
        this.el.questionText.textContent   = q.text;

        // Options
        this.el.optionsContainer.innerHTML = '';
        ['A','B','C','D'].forEach(label => {
            if (!q.options[label]) return;
            const div = document.createElement('div');
            div.className = 'option';
            if (this.state.getAnswer(q.id) === label) div.classList.add('selected');
            div.innerHTML = `<div class="option-label">${label}</div><div class="option-text">${q.options[label]}</div>`;
            div.addEventListener('click', () => { this.state.setAnswer(q.id, label); this.render(); });
            this.el.optionsContainer.appendChild(div);
        });

        // Flag button state
        const flagged = this.state.isFlagged(q.id);
        this.el.flagBtn.classList.toggle('flagged', flagged);
        const fi = this.el.flagBtn.querySelector('i');
        if (fi) { fi.className = flagged ? 'fas fa-flag' : 'far fa-flag'; }

        // Nav buttons
        this.el.prevBtn.disabled = this.state.currentQuestionIndex === 0;
        const isLast = this.state.currentQuestionIndex === this.state.questions.length - 1;
        this.el.nextBtn.innerHTML = isLast
            ? '<i class="fas fa-check"></i> Review &amp; Submit'
            : 'Next <i class="fas fa-arrow-right"></i>';
    }

    _renderStats() {
        this.el.answeredCount.textContent   = this.state.getAnsweredCount();
        this.el.unansweredCount.textContent = this.state.getUnansweredCount();
        this.el.flaggedCount.textContent    = this.state.getFlaggedCount();
    }

    // ── Timer ──
    _startTimer() {
        this.state.startTimer(
            t => this._tickTimer(t),
            () => this._timeUp()
        );
    }

    _tickTimer(t) {
        this.el.timerDisplay.textContent = this.state.formatTime(t);

        const offset = 163.36 - (t / this.state.duration) * 163.36;
        this.el.timerProgressCircle.style.strokeDashoffset = offset;

        const tc = this.el.timerContainer;
        const td = this.el.timerDisplay;
        tc && tc.classList.remove('warning','danger');
        td.classList.remove('warning','danger');

        if (t <= 60) {
            tc && tc.classList.add('danger');
            td.classList.add('danger');
            this.el.timerProgressCircle.style.stroke = 'var(--red, #ef4444)';
        } else if (t <= 300) {
            tc && tc.classList.add('warning');
            td.classList.add('warning');
            this.el.timerProgressCircle.style.stroke = '#fbbf24';
        }
    }

    // ── Actions ──
    _prev()         { if (this.state.prevQuestion()) this.render(); }
    _next()         { this.state.currentQuestionIndex === this.state.questions.length - 1 ? this._showSubmitModal() : (this.state.nextQuestion() && this.render()); }
    _clearAnswer()  { this.state.clearAnswer(this.state.getCurrentQuestion().id); this.render(); }
    _toggleFlag()   { this.state.toggleFlag(this.state.getCurrentQuestion().id); this.render(); }

    _toggleSidebar()     { this.el.sidebar.classList.toggle('open'); }
    _closeSidebarMobile(){ if (window.innerWidth <= 1024) this.el.sidebar.classList.remove('open'); }

    _showSubmitModal() {
        document.getElementById('modalTotalQuestions').textContent  = this.state.questions.length;
        document.getElementById('modalAnsweredCount').textContent   = this.state.getAnsweredCount();
        document.getElementById('modalUnansweredCount').textContent = this.state.getUnansweredCount();
        document.getElementById('modalTimeRemaining').textContent   = this.state.formatTime(this.state.timeRemaining);
        this.el.submitModal.classList.remove('hidden');
    }
    _hideSubmitModal() { this.el.submitModal.classList.add('hidden'); }

    _showCalc()  { this.el.calculatorModal.classList.remove('hidden'); }
    _hideCalc()  { this.el.calculatorModal.classList.add('hidden'); }

    _submit() {
        this.state.isSubmitted = true;
        this.state.stopTimer();
        this._hideSubmitModal();
        this._showResults();
    }

    _timeUp() {
        this.state.isSubmitted = true;
        this.el.timeUpModal && this.el.timeUpModal.classList.remove('hidden');
    }

    _showResults() {
        const s      = this.state.getScore();
        const pct    = s.percentage;
        const grade  = pct >= 70 ? 'EXCELLENT' : pct >= 50 ? 'AVERAGE' : 'NEEDS WORK';
        const today  = new Date().toISOString().slice(0, 10);
        const meta   = window.quizMetadata || {};
        const subject   = meta.subject   || this.state.questions[0]?.subject || 'Practice Test';
        const timeTaken = this._formatTimeTaken(this.state.duration - this.state.timeRemaining);

        const rows = this.state.questions.map((q, i) => {
            const yours   = this.state.getAnswer(q.id) || '—';
            const correct = q.answer;
            const isRight = yours === correct;
            const shortText = q.text.length > 55 ? q.text.slice(0, 52) + '…' : q.text;

            const explanationRow = (!isRight && q.explanation)
                ? `<tr class="expl-row">
                     <td></td>
                     <td colspan="3" class="explanation-cell">
                       <span class="expl-label">Explanation:</span> ${q.explanation}
                       ${q.exception ? `<br><span class="expl-label">Note:</span> ${q.exception}` : ''}
                     </td>
                   </tr>`
                : '';

            return `
              <tr class="${isRight ? 'row-correct' : 'row-wrong'}">
                <td class="col-num">${i + 1}</td>
                <td class="col-q">${shortText}</td>
                <td class="col-ans ${isRight ? '' : 'wrong-ans'}">${yours}</td>
                <td class="col-correct">${correct} <span class="status-symbol">${isRight ? '✓' : '✗'}</span></td>
              </tr>
              ${explanationRow}`;
        }).join('');

        const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Results — ${subject}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Helvetica Neue', Arial, sans-serif; background: #fff; color: #111; padding: 2.5rem; max-width: 820px; margin: 0 auto; font-size: 13px; }
    .report-header { margin-bottom: 1.5rem; }
    .brand { font-size: 1.1rem; font-weight: 800; letter-spacing: -0.02em; color: #111; }
    .brand span { color: #f59e0b; }
    .report-title { font-size: 0.8rem; color: #666; margin-top: 0.15rem; }
    .score-card { display: flex; align-items: center; gap: 2rem; padding: 1.25rem 1.5rem; border: 2px solid #111; border-radius: 10px; margin-bottom: 1.5rem; background: #fafafa; }
    .score-big { font-size: 2.75rem; font-weight: 800; line-height: 1; letter-spacing: -0.04em; }
    .score-big.excellent { color: #059669; }
    .score-big.average   { color: #d97706; }
    .score-big.poor      { color: #dc2626; }
    .score-details { flex: 1; }
    .score-line { font-size: 1rem; font-weight: 700; margin-bottom: 0.15rem; }
    .score-meta { font-size: 0.78rem; color: #555; line-height: 1.7; }
    .score-meta strong { color: #111; }
    .grade-badge { font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em; padding: 0.3rem 0.75rem; border-radius: 999px; text-transform: uppercase; }
    .grade-badge.excellent { background: #d1fae5; color: #065f46; }
    .grade-badge.average   { background: #fef3c7; color: #92400e; }
    .grade-badge.poor      { background: #fee2e2; color: #991b1b; }
    .section-title { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #888; margin-bottom: 0.6rem; }
    table { width: 100%; border-collapse: collapse; }
    thead th { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #888; border-bottom: 2px solid #111; padding: 0.4rem 0.5rem; text-align: left; }
    tbody tr.row-correct td { background: #f0fdf4; }
    tbody tr.row-wrong   td { background: #fff7f7; }
    tbody td { padding: 0.45rem 0.5rem; border-bottom: 1px solid #e5e7eb; vertical-align: top; line-height: 1.5; }
    .col-num { width: 32px; color: #888; font-size: 0.75rem; }
    .col-ans { width: 52px; text-align: center; font-weight: 700; }
    .col-correct { width: 72px; text-align: center; font-weight: 700; color: #059669; }
    .wrong-ans { color: #dc2626; }
    tr.expl-row td { background: #fffbeb !important; border-bottom: 1px solid #fde68a; padding: 0.4rem 0.5rem 0.6rem 2rem; }
    .explanation-cell { font-size: 0.78rem; color: #555; line-height: 1.6; }
    .expl-label { font-weight: 700; color: #92400e; }
    .report-footer { margin-top: 1.5rem; padding-top: 0.75rem; border-top: 1px solid #e5e7eb; display: flex; justify-content: space-between; font-size: 0.72rem; color: #aaa; }
    @media print { body { padding: 1.5rem; } .no-print { display: none !important; } }
  </style>
</head>
<body>
  <div class="report-header">
    <div class="brand">Grant<span>App</span> AI</div>
    <div class="report-title">JAMB Practice Test Results — ${today}</div>
  </div>
  <div class="score-card">
    <div class="score-big ${pct >= 70 ? 'excellent' : pct >= 50 ? 'average' : 'poor'}">${pct.toFixed(1)}%</div>
    <div class="score-details">
      <div class="score-line">${s.correct} / ${s.total} Correct</div>
      <div class="score-meta"><strong>${subject}</strong><br>Time taken: ${timeTaken}</div>
    </div>
    <div class="grade-badge ${pct >= 70 ? 'excellent' : pct >= 50 ? 'average' : 'poor'}">${grade}</div>
  </div>
  <div class="section-title">Question Breakdown</div>
  <table>
    <thead><tr><th>#</th><th>Question</th><th style="text-align:center">Yours</th><th style="text-align:center">Answer</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>
  <div class="report-footer">
    <span>GrantApp AI &nbsp;·&nbsp; 100 Days to UTME</span>
    <span>Page 1 of 1</span>
  </div>
  <div class="no-print" style="text-align:center;margin-top:2rem;">
    <button onclick="window.print()" style="padding:0.65rem 1.5rem;background:#f59e0b;color:#000;border:none;border-radius:8px;font-weight:700;font-size:0.9rem;cursor:pointer;margin-right:0.75rem;">Save as PDF</button>
    <button onclick="history.back()" style="padding:0.65rem 1.5rem;background:#f3f4f6;color:#111;border:1px solid #d1d5db;border-radius:8px;font-weight:600;font-size:0.9rem;cursor:pointer;">← Back</button>
  </div>
</body>
</html>`;

        document.open();
        document.write(html);
        document.close();
    }

    _formatTimeTaken(seconds) {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    }

    _handleCalc(e) {
        const btn     = e.currentTarget;
        const display = document.getElementById('calcDisplay');
        const val     = btn.dataset.value;
        const action  = btn.dataset.action;
        if (val) {
            display.value = display.value === '0' ? val : display.value + val;
        } else if (action) {
            switch (action) {
                case 'clear':    display.value = '0'; break;
                case 'delete':   display.value = display.value.slice(0,-1) || '0'; break;
                case 'add': case 'subtract': case 'multiply': case 'divide':
                    display.value += ' ' + btn.textContent + ' '; break;
                case 'equals':
                    try {
                        display.value = eval(display.value.replace(/×/g,'*').replace(/÷/g,'/').replace(/−/g,'-'));
                    } catch { display.value = 'Error'; setTimeout(() => display.value = '0', 1000); }
                    break;
            }
        }
    }

    _keyboard(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        const map = { ArrowLeft: () => this._prev(), ArrowRight: () => this._next(),
                      a:'A', b:'B', c:'C', d:'D', A:'A', B:'B', C:'C', D:'D',
                      f: () => this._toggleFlag(), F: () => this._toggleFlag(),
                      Escape: () => { this._hideSubmitModal(); this._hideCalc(); } };
        const v = map[e.key];
        if (!v) return;
        e.preventDefault();
        if (typeof v === 'function') v();
        else { this.state.setAnswer(this.state.getCurrentQuestion().id, v); this.render(); }
    }
}

// ── Boot ────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    if (typeof QUESTIONS === 'undefined' || !QUESTIONS.length) {
        document.body.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;height:100vh;background:#0a0a0f;color:#f0eff4;font-family:sans-serif;text-align:center;padding:2rem"><div><div style="font-size:3rem;margin-bottom:1rem">⚠️</div><h2 style="margin-bottom:0.5rem">No Questions Found</h2><p style="color:#7a7a8c;margin-bottom:1.5rem">QUESTIONS array is not defined on this page.</p><button onclick="history.back()" style="padding:0.6rem 1.2rem;background:#f59e0b;color:#000;border:none;border-radius:8px;font-weight:700;cursor:pointer">← Go Back</button></div></div>`;
        return;
    }

    const duration  = typeof DURATION !== 'undefined' ? DURATION : 900;
    const quizState = new QuizState(QUESTIONS, duration);
    const quizUI    = new QuizUI(quizState);

    window.addEventListener('beforeunload', e => {
        if (!quizState.isSubmitted) { e.preventDefault(); e.returnValue = ''; }
    });
});
