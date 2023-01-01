#!/usr/bin/env python3
"""
Script para pintar el nombre RAZTOR en el contribution chart de GitHub.
"""

import os
import subprocess
import re
from datetime import datetime, timedelta

AUTO_ADJUST = True
COMMITS_PER_DAY = 15
INTENSITY_MULTIPLIER = 2.5

LETTER_R = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
]

LETTER_A = [
    [0, 1, 1, 1, 0],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
]

LETTER_Z = [
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
]

LETTER_T = [
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
]

LETTER_O = [
    [0, 1, 1, 1, 0],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0],
]

WORD = [LETTER_R, LETTER_A, LETTER_Z, LETTER_T, LETTER_O, LETTER_R]
SPACE_BETWEEN_LETTERS = 1


def get_sunday_of_week(target_date):
    """Obtiene el domingo de la semana de una fecha dada"""
    days_since_sunday = (target_date.weekday() + 1) % 7
    return target_date - timedelta(days=days_since_sunday)


def analyze_commit_intensity():
    """Analiza los commits en el último año"""
    try:
        one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        result = subprocess.run(
            ['git', 'log', '--all', '--oneline', '--since', one_year_ago],
            capture_output=True,
            text=True,
            check=True
        )
        
        commit_lines = result.stdout.strip().split('\n')
        total_commits = len([line for line in commit_lines if line])
        
        if total_commits == 0:
            return None
        
        avg_per_day = total_commits / 365.0
        
        print(f"📊 Análisis de commits en el último año:")
        print(f"   Total de commits: {total_commits}")
        print(f"   Promedio por día: {avg_per_day:.2f}")
        
        return avg_per_day
        
    except:
        return None


def calculate_commits_per_day(auto_adjust=True, manual_value=15, multiplier=2.5):
    """Calcula cuántos commits hacer por día"""
    if auto_adjust:
        avg = analyze_commit_intensity()
        
        if avg is not None:
            recommended = int(avg * multiplier)
            recommended = max(10, min(recommended, 25))
            
            print(f"   Recomendado: {recommended} commits/día (promedio × {multiplier})")
            
            return recommended
        else:
            print(f"⚠️  No se pudo calcular automáticamente")
    
    print(f"📌 Usando valor manual: {manual_value} commits/día")
    return manual_value


def calculate_positions():
    """
    Calcula las posiciones para que RAZTOR aparezca centrado en los últimos 365 días.
    
    GitHub muestra aproximadamente 52 semanas desde el domingo más reciente.
    """
    positions = []
    
    today = datetime.now()
    
    current_sunday = get_sunday_of_week(today)
    
    github_start = current_sunday - timedelta(weeks=52)
    
    total_width = sum(len(letter[0]) for letter in WORD) + SPACE_BETWEEN_LETTERS * (len(WORD) - 1)
    
    margin_left = 8
    pattern_start = github_start + timedelta(weeks=margin_left)
    
    current_column = 0
    
    for letter_idx, letter in enumerate(WORD):
        letter_width = len(letter[0])
        
        for col in range(letter_width):
            for row in range(7):
                if letter[row][col] == 1:
                    commit_date = pattern_start + timedelta(weeks=current_column, days=row)
                    
                    if github_start <= commit_date <= today:
                        positions.append(commit_date)
        
        current_column += letter_width + SPACE_BETWEEN_LETTERS
    
    return positions


def make_commit(commit_date, commits_per_day):
    """Crea múltiples commits vacíos en una fecha específica"""
    hours = list(range(8, 24))
    
    for i in range(commits_per_day):
        hour_index = i % len(hours)
        hour = hours[hour_index]
        minute = (i * 3) % 60
        second = (i * 7) % 60
        
        commit_datetime = commit_date.replace(hour=hour, minute=minute, second=second)
        date_str = commit_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        os.environ['GIT_AUTHOR_DATE'] = date_str
        os.environ['GIT_COMMITTER_DATE'] = date_str
        
        try:
            subprocess.run(
                ['git', 'commit', '--allow-empty', '-m', f'RAZTOR {commit_date.strftime("%Y-%m-%d")} #{i+1}'],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            return False
    
    return True


def main():
    """Función principal"""
    print("=" * 70)
    print("🎨 RAZTOR GitHub Contribution Painter")
    print("=" * 70)
    print()
    
    commits_per_day = calculate_commits_per_day(
        auto_adjust=AUTO_ADJUST,
        manual_value=COMMITS_PER_DAY,
        multiplier=INTENSITY_MULTIPLIER
    )
    
    print()
    print("=" * 70)
    print("Calculando posiciones para RAZTOR...")
    positions = calculate_positions()
    
    total_commits = len(positions) * commits_per_day
    print(f"\n📝 Resumen:")
    print(f"   Días con patrón: {len(positions)}")
    print(f"   Commits por día: {commits_per_day}")
    print(f"   Total de commits: {total_commits}")
    print(f"   Rango: {min(positions).date()} a {max(positions).date()}")
    print()
    
    intensity_level = "BAJO" if commits_per_day < 10 else "MEDIO" if commits_per_day < 20 else "ALTO"
    print(f"   Nivel de intensidad: {intensity_level}")
    print()
    print("=" * 70)
    print()
    
    success_count = 0
    for idx, position in enumerate(positions, 1):
        print(f"[{idx}/{len(positions)}] {position.strftime('%Y-%m-%d')}... ", end="", flush=True)
        if make_commit(position, commits_per_day):
            success_count += 1
            print(f"✓ {commits_per_day} commits")
        else:
            print("✗ Error")
    
    print()
    print("=" * 70)
    print(f"✅ Completado: {success_count}/{len(positions)} días procesados")
    print(f"📊 Total de commits creados: {success_count * commits_per_day}")
    print("=" * 70)


if __name__ == "__main__":
    main()
